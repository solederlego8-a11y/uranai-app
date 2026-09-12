/* =========================================================================
 * 今日の総合鑑定 — 静的サイト版のフォーム／結果描画
 *
 *  index.html  : URLパラメータからフォームを復元し、入力エラーがあれば表示する
 *  result.html : URLパラメータ → Uranai.validate → Uranai.buildReport → DOM描画
 *
 *  占術ロジック本体は js/uranai.js（グローバル Uranai）が提供する。
 *  レーダーチャートとアコーディオンの初期化は js/main.js が行う。
 * ========================================================================= */
(function () {
  "use strict";

  var lang = (document.documentElement.lang || "").toLowerCase().indexOf("en") === 0 ? "en" : "ja";
  var isEnglish = lang === "en";
  var page = document.body.getAttribute("data-page");
  var FIELDS = ["last_name", "first_name", "birth_year", "birth_month", "birth_day",
                "birth_hour", "gender", "prefecture"];
  var YEAR_MIN = 1900;
  // 個別相談への誘導（A8.net ココナラ電話占い）。href が空の間は描画しない。
  // A8 に当サイトを登録し、そのサイト向けに生成した a8mat リンクを設定すること。
  var CONSULT_CTA = {
    href: "",
    pixel: ""
  };
  var MONTHS_EN =["January", "February", "March", "April", "May", "June", "July",
                   "August", "September", "October", "November", "December"];
  var TEXT = isEnglish
    ? {
        engineMissing: "The reading engine could not be loaded. Please reload the page and try again.",
        reportFailed: "Something went wrong while generating your reading. Please try again.",
        hourUnknown: "Unknown (calculated as noon)",
        prefUnknown: "Unknown / overseas (Tokyo used as a substitute)",
        genderFallback: "Prefer not to say"
      }
    : {
        engineMissing: "鑑定エンジンを読み込めませんでした。ページを再読み込みしてもう一度お試しください。",
        reportFailed: "鑑定中に問題が発生しました。お手数ですが、もう一度お試しください。",
        hourUnknown: "不明（正午として計算）",
        prefUnknown: "不明・海外（東京で代替）",
        genderFallback: "回答しない"
      };
  var GENDER_JA = { male: "男性", female: "女性", unknown: "回答しない" };

  /* ------------------------------------------------------------------ */
  /* 共通ユーティリティ                                                   */
  /* ------------------------------------------------------------------ */
  function esc(value) {
    return String(value === null || value === undefined ? "" : value)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  function pad2(n) {
    return (n < 10 ? "0" : "") + n;
  }

  // Date / "YYYY-MM-DD" / {year, month, day} のいずれでも {year, month, day} に揃える
  function toYMD(value) {
    if (!value) {
      return null;
    }
    if (value instanceof Date) {
      return { year: value.getFullYear(), month: value.getMonth() + 1, day: value.getDate() };
    }
    if (typeof value === "string") {
      var m = /^(\d{4})-(\d{1,2})-(\d{1,2})/.exec(value);
      return m ? { year: +m[1], month: +m[2], day: +m[3] } : null;
    }
    if (typeof value === "object" && value.year !== undefined) {
      return { year: +value.year, month: +value.month, day: +value.day };
    }
    return null;
  }

  function jstToday() {
    var ymd = null;
    if (window.Uranai && typeof window.Uranai.todayJst === "function") {
      ymd = toYMD(window.Uranai.todayJst());
    }
    if (!ymd) {
      var d = new Date(Date.now() + 9 * 60 * 60 * 1000);
      ymd = { year: d.getUTCFullYear(), month: d.getUTCMonth() + 1, day: d.getUTCDate() };
    }
    return ymd;
  }

  function formatDateJa(ymd) {
    return ymd.year + "年" + ymd.month + "月" + ymd.day + "日";
  }

  // Python の strftime('%B %d, %Y') と同じ（日は2桁ゼロ埋め）
  function formatDateEn(ymd) {
    return MONTHS_EN[ymd.month - 1] + " " + pad2(ymd.day) + ", " + ymd.year;
  }

  // Jinja2 の {{ value }} が dict / list / bool / None に対して出す Python 表記を再現する
  function pyRepr(value, nested) {
    if (value === null || value === undefined) {
      return "None";
    }
    if (value === true) {
      return "True";
    }
    if (value === false) {
      return "False";
    }
    if (typeof value === "number") {
      return String(value);
    }
    if (typeof value === "string") {
      return nested ? "'" + value.replace(/\\/g, "\\\\").replace(/'/g, "\\'") + "'" : value;
    }
    if (Array.isArray(value)) {
      return "[" + value.map(function (v) { return pyRepr(v, true); }).join(", ") + "]";
    }
    if (typeof value === "object") {
      return "{" + Object.keys(value).map(function (k) {
        return pyRepr(k, true) + ": " + pyRepr(value[k], true);
      }).join(", ") + "}";
    }
    return String(value);
  }

  function readParams() {
    var params = new URLSearchParams(window.location.search);
    var values = {};
    var present = false;
    FIELDS.forEach(function (key) {
      if (params.has(key)) {
        present = true;
      }
      values[key] = params.get(key) || "";
    });
    return { values: values, present: present, raw: params };
  }

  function indexHref() {
    return "./";
  }

  function showAlert(container, message) {
    var box = document.getElementById("form-alert");
    if (!box) {
      box = document.createElement("div");
      box.className = "alert";
      box.setAttribute("role", "alert");
      (container || document.querySelector("main.container")).insertBefore(
        box, (container || document.querySelector("main.container")).firstChild);
    }
    box.textContent = message;
    box.hidden = false;
  }

  /* ------------------------------------------------------------------ */
  /* index.html                                                          */
  /* ------------------------------------------------------------------ */
  function ensureYearOptions(select, maxYear) {
    var first = select.options.length > 1 ? parseInt(select.options[1].value, 10) : NaN;
    if (isNaN(first) || first >= maxYear) {
      return;
    }
    for (var y = first + 1; y <= maxYear; y++) {
      var opt = document.createElement("option");
      opt.value = String(y);
      opt.textContent = isEnglish ? String(y) : y + "年";
      select.insertBefore(opt, select.options[1]);
    }
  }

  function fillForm(form, values) {
    FIELDS.forEach(function (key) {
      var field = form.elements[key];
      if (!field) {
        return;
      }
      var value = values[key];
      if (typeof RadioNodeList !== "undefined" && field instanceof RadioNodeList) {
        var chosen = value || "unknown";
        Array.prototype.forEach.call(field, function (radio) {
          radio.checked = radio.value === chosen;
        });
      } else if (field.tagName === "SELECT") {
        var hasOption = Array.prototype.some.call(field.options, function (o) {
          return o.value === value;
        });
        if (hasOption) {
          field.value = value;
        }
      } else {
        field.value = value;
      }
    });
  }

  function initIndex() {
    var today = jstToday();
    var dateNode = document.getElementById("hero-date");
    if (dateNode) {
      dateNode.textContent = isEnglish ? "Today is " + formatDateEn(today)
                                       : "本日は " + formatDateJa(today) + "です";
    }
    var form = document.getElementById("uranai-form");
    if (!form) {
      return;
    }
    var yearSelect = form.elements.birth_year;
    if (yearSelect) {
      ensureYearOptions(yearSelect, today.year);
    }

    var params = readParams();
    if (!params.present) {
      return;
    }
    // result.html から差し戻された場合：入力を復元し、同じ検証でエラー文を表示する
    fillForm(form, params.values);
    if (window.Uranai && typeof window.Uranai.validate === "function") {
      var checked = window.Uranai.validate(params.values, lang);
      if (checked && checked.error) {
        showAlert(null, checked.error);
      }
    }
  }

  /* ------------------------------------------------------------------ */
  /* result.html — 入力内容のラベル（app.py の result() / result_en()）   */
  /* ------------------------------------------------------------------ */
  function labelsJa(userData) {
    var prefectures = (window.Uranai && window.Uranai.PREFECTURES) || [];
    return {
      gender: GENDER_JA[userData.gender] || TEXT.genderFallback,
      hour: (userData.birth_hour === null || userData.birth_hour === undefined)
        ? TEXT.hourUnknown : userData.birth_hour + "時台",
      prefecture: prefectures.indexOf(userData.prefecture) >= 0
        ? userData.prefecture : TEXT.prefUnknown
    };
  }

  function labelsEn(userData) {
    var U = window.Uranai || {};
    var prefectures = U.PREFECTURES || [];
    var cities = U.WORLD_CITIES || [];
    var pref = userData.prefecture;
    var prefLabel;
    if (prefectures.indexOf(pref) >= 0) {
      prefLabel = typeof U.prefectureEn === "function" ? U.prefectureEn(pref) : pref;
    } else if (cities.indexOf(pref) >= 0) {
      prefLabel = typeof U.worldCityLabel === "function" ? U.worldCityLabel(pref) : pref;
    } else {
      prefLabel = TEXT.prefUnknown;
    }
    return {
      gender: (U.GENDER_EN && U.GENDER_EN[userData.gender]) || TEXT.genderFallback,
      hour: (userData.birth_hour === null || userData.birth_hour === undefined)
        ? TEXT.hourUnknown : userData.birth_hour + ":00",
      prefecture: prefLabel
    };
  }

  function moduleCount(report) {
    var U = window.Uranai || {};
    if (U.MODULES && U.MODULES.length) {
      return U.MODULES.length;
    }
    return (report.detail_results || []).length || 11;
  }

  function scoreDataScript(breakdown) {
    // JSON を <script type="application/json"> に埋め込む（main.js が読み取る）
    var json = JSON.stringify(breakdown).replace(/</g, "\\u003c");
    return '<script id="score-data" type="application/json">' + json + "</script>";
  }

  /* ------------------------------------------------------------------ */
  /* result.html（日本語）— templates/result.html の描画を移植            */
  /* ------------------------------------------------------------------ */
  // シェアURLは氏名・生年月日を含む結果URLではなくトップページを使う
  var SITE_JA = "https://solederlego8-a11y.github.io/uranai-app/";
  var SITE_EN = "https://solederlego8-a11y.github.io/uranai-app/en/";

  function shareLinks(text, url, hashtags) {
    var x = "https://twitter.com/intent/tweet?text=" + encodeURIComponent(text) +
      "&url=" + encodeURIComponent(url) + (hashtags ? "&hashtags=" + encodeURIComponent(hashtags) : "");
    var line = "https://social-plugins.line.me/lineit/share?url=" + encodeURIComponent(url) +
      "&text=" + encodeURIComponent(text);
    return { x: x, line: line };
  }

  function shareBlockJa(report, today) {
    var text = formatDateJa(today) + "の総合鑑定は【" + report.score_rank + "】" + report.total_score + "点。" +
      "ラッキーカラーは" + report.lucky_color + "、ラッキーアイテムは" + report.lucky_item + "。" +
      "11種の占術をまとめて鑑定できます。";
    var links = shareLinks(text, SITE_JA, "今日の総合鑑定");
    return [
      '  <div class="share-block">',
      '    <p class="share-title">結果をシェアする</p>',
      '    <div class="share-buttons">',
      '      <a class="share-btn share-x" href="' + esc(links.x) + '" target="_blank" rel="noopener" data-share="x">Xでシェア</a>',
      '      <a class="share-btn share-line" href="' + esc(links.line) + '" target="_blank" rel="noopener" data-share="line">LINEで送る</a>',
      "    </div>",
      '    <p class="share-note">お名前や生年月日は含まれません。共有されるのは結果の要約とサイトのURLだけです。</p>',
      '    <p class="return-note">運勢は日付ごとに変わります。<a href="' + esc(SITE_JA) + '">明日もう一度占う</a>ときのために、このサイトをブックマークしておくと便利です。</p>',
      "  </div>"
    ].join("\n");
  }

  function shareBlockEn(report, today) {
    var text = "My reading for " + formatDateEn(today) + ": " + (report.score_rank_en || report.score_rank) +
      " (" + report.total_score + "/100). Lucky color " + (report.lucky_color_en || report.lucky_color) +
      ", lucky item " + (report.lucky_item_en || report.lucky_item) + ". 11 divination systems in one reading.";
    var links = shareLinks(text, SITE_EN, "TodaysFortune");
    return [
      '  <div class="share-block">',
      '    <p class="share-title">Share your reading</p>',
      '    <div class="share-buttons">',
      '      <a class="share-btn share-x" href="' + esc(links.x) + '" target="_blank" rel="noopener" data-share="x">Share on X</a>',
      '      <a class="share-btn share-line" href="' + esc(links.line) + '" target="_blank" rel="noopener" data-share="line">Share on LINE</a>',
      "    </div>",
      '    <p class="share-note">Your name and birth date are not included. Only the summary and the site URL are shared.</p>',
      '    <p class="return-note">Readings change every day. Bookmark this site to <a href="' + esc(SITE_EN) + '">come back tomorrow</a>.</p>',
      "  </div>"
    ].join("\n");
  }

  function renderResultJa(report, userData, today) {
    var U = window.Uranai || {};
    var categoryLabel = U.CATEGORY_LABEL || { love: "恋愛運", work: "仕事運", money: "金運", health: "健康運" };
    var labels = labelsJa(userData);
    var h = [];

    h.push('<section class="verdict" id="verdict">');
    h.push('  <p class="verdict-eyebrow">' + esc(formatDateJa(today)) + 'の総合鑑定</p>');
    h.push('  <h1 class="verdict-name">' + esc(userData.last_name) + " " + esc(userData.first_name) + ' さん</h1>');
    h.push('  <div class="verdict-main">');
    h.push('    <div class="rank-badge rank-' + esc(report.score_rank) + '">');
    h.push('      <span class="rank-label">総合</span>');
    h.push('      <span class="rank-value">' + esc(report.score_rank) + "</span>");
    h.push("    </div>");
    h.push('    <div class="score-block">');
    h.push('      <div class="score-number">');
    h.push('        <span class="score-value">' + esc(report.total_score) + '</span><span class="score-unit">/ 100点</span>');
    h.push("      </div>");
    h.push('      <div class="progress" role="img" aria-label="総合スコア ' + esc(report.total_score) + '点">');
    h.push('        <div class="progress-bar" style="width: ' + esc(report.total_score) + '%"></div>');
    h.push("      </div>");
    h.push('      <p class="score-note">' + moduleCount(report) + "種の占術の重み付き平均で算出しています。</p>");
    h.push("    </div>");
    h.push("  </div>");

    h.push('  <div class="lucky-grid">');
    h.push('    <div class="lucky-item">');
    h.push('      <p class="lucky-label">ラッキーカラー</p>');
    h.push('      <p class="lucky-value"><span class="color-chip" style="background: ' + esc(report.lucky_color_hex) + '"></span> ' + esc(report.lucky_color) + "</p>");
    h.push('      <p class="lucky-sub">' + esc(report.lucky_color_hex) + "</p>");
    h.push("    </div>");
    h.push('    <div class="lucky-item"><p class="lucky-label">ラッキーアイテム</p><p class="lucky-value">' + esc(report.lucky_item) + "</p></div>");
    h.push('    <div class="lucky-item"><p class="lucky-label">ラッキー方位</p><p class="lucky-value">' + esc(report.lucky_dir) + "</p></div>");
    h.push('    <div class="lucky-item"><p class="lucky-label">ラッキーナンバー</p><p class="lucky-value">' + esc(report.lucky_number) + "</p></div>");
    h.push("  </div>");

    h.push('  <div class="message-block">');
    h.push('    <h2 class="block-title">今日の総合アドバイス</h2>');
    h.push('    <p class="overall-message">' + esc(report.overall_message) + "</p>");
    h.push("  </div>");

    if (report.today_keywords && report.today_keywords.length) {
      h.push('  <div class="keyword-block">');
      h.push('    <h2 class="block-title">今日のキーワード</h2>');
      h.push('    <ul class="keyword-list">');
      report.today_keywords.forEach(function (kw) {
        h.push('      <li class="keyword-tag">' + esc(kw) + "</li>");
      });
      h.push("    </ul>");
      h.push("  </div>");
    }

    h.push('  <div class="category-block">');
    h.push('    <h2 class="block-title">カテゴリ別の運勢</h2>');
    h.push('    <ul class="category-list">');
    ["love", "work", "money", "health"].forEach(function (key) {
      var value = report.category_scores[key];
      h.push('      <li class="category-row">');
      h.push('        <span class="category-name">' + esc(categoryLabel[key]) + "</span>");
      h.push('        <span class="category-bar"><span class="category-fill category-' + key + '" style="width: ' + esc(value) + '%"></span></span>');
      h.push('        <span class="category-value">' + esc(value) + "</span>");
      h.push("      </li>");
    });
    h.push("    </ul>");
    h.push("  </div>");

    h.push(shareBlockJa(report, today));

    h.push('  <p class="verdict-disclaimer">※本鑑定はエンターテインメントを目的としたものであり、科学的根拠を保証するものではありません。</p>');
    h.push("</section>");

    h.push("<!-- ADSENSE_SLOT -->");
    h.push('<div class="ad-container ad-result-1">広告スペース</div>');

    h.push('<section class="card chart-card">');
    h.push('  <h2 class="card-title">11種の占術スコア</h2>');
    h.push('  <div class="chart-wrap">');
    h.push('    <canvas id="scoreRadar" width="400" height="400" aria-label="11種の占術スコアのレーダーチャート" role="img"></canvas>');
    h.push("  </div>");
    h.push('  <ul class="score-fallback" hidden>');
    Object.keys(report.score_breakdown).forEach(function (name) {
      h.push("    <li>" + esc(name) + "：" + esc(report.score_breakdown[name]) + "点</li>");
    });
    h.push("  </ul>");
    h.push("  " + scoreDataScript(report.score_breakdown));
    h.push("</section>");

    h.push('<section class="detail-section">');
    h.push('  <h2 class="section-title">詳しく見る（11種の個別鑑定）</h2>');
    h.push('  <p class="section-note">それぞれの占術がどう読み解いたのかを確認できます。項目をタップすると開きます。</p>');
    h.push('  <div class="accordion">');
    (report.detail_results || []).forEach(function (item) {
      h.push('    <details class="accordion-item">');
      h.push('      <summary class="accordion-head">');
      h.push('        <span class="accordion-title">' + esc(item.name) + "</span>");
      h.push('        <span class="accordion-score">' + esc(item.score) + "点</span>");
      h.push('        <span class="accordion-icon" aria-hidden="true"></span>');
      h.push("      </summary>");
      h.push('      <div class="accordion-body">');
      h.push('        <p class="item-summary">' + esc(item.summary) + "</p>");
      h.push('        <div class="item-meter"><span class="item-meter-fill" style="width: ' + esc(item.score) + '%"></span></div>');
      h.push('        <p class="item-detail">' + esc(item.detail) + "</p>");
      h.push('        <ul class="item-lucky">');
      h.push("          <li><span>色</span>" + esc(item.lucky_color) + "</li>");
      h.push("          <li><span>物</span>" + esc(item.lucky_item) + "</li>");
      h.push("          <li><span>方位</span>" + esc(item.lucky_dir) + "</li>");
      h.push("        </ul>");
      if (item.keywords && item.keywords.length) {
        h.push('        <ul class="item-keywords">');
        item.keywords.forEach(function (kw) {
          h.push("          <li>" + esc(kw) + "</li>");
        });
        h.push("        </ul>");
      }
      if (item.raw && Object.keys(item.raw).length) {
        h.push('        <details class="raw-data">');
        h.push("          <summary>算出データを見る</summary>");
        h.push('          <dl class="raw-list">');
        Object.keys(item.raw).forEach(function (key) {
          h.push('            <div class="raw-row"><dt>' + esc(key) + "</dt><dd>" + esc(pyRepr(item.raw[key], false)) + "</dd></div>");
        });
        h.push("          </dl>");
        h.push("        </details>");
      }
      h.push("      </div>");
      h.push("    </details>");
    });
    h.push("  </div>");
    h.push("</section>");

    if (CONSULT_CTA.href) {
      h.push('<section class="card consult-card">');
      h.push('  <p class="consult-label">この結果をもっと深く知りたい方へ</p>');
      h.push('  <h2 class="card-title">恋愛・仕事の具体的な悩みは、占い師に直接相談できます</h2>');
      h.push('  <p class="consult-text">今日の鑑定は、お名前と生年月日から11種の占術を機械的に算出した自動鑑定です。「この結果は自分の状況にどう当てはまるのか」「今の悩みに対して具体的にどう動けばいいのか」といった個別の相談は、実力派の占い師に電話で直接聞けるサービスがあります。初回は最大30分無料で試せるため、まず一度話してみてから続けるかどうかを決められます。</p>');
      h.push('  <a class="submit-button link-button consult-button" href="' + esc(CONSULT_CTA.href) + '" rel="nofollow sponsored" target="_blank">電話占いで個別に相談する（初回最大30分無料）</a>');
      if (CONSULT_CTA.pixel) {
        h.push('  <img src="' + esc(CONSULT_CTA.pixel) + '" width="1" height="1" alt="" style="border:0">');
      }
      h.push('  <p class="consult-note">※外部サービス（ココナラ）のページに移動します。当サイトはプロモーションを含みます。</p>');
      h.push("</section>");
    } else {
      h.push("<!-- ADSENSE_SLOT -->");
      h.push('<div class="ad-container ad-result-2">広告スペース</div>');
    }

    h.push('<section class="card input-card">');
    h.push('  <h2 class="card-title">今回の鑑定に使用した入力</h2>');
    h.push('  <dl class="input-list">');
    h.push('    <div class="input-row"><dt>お名前</dt><dd>' + esc(userData.last_name) + " " + esc(userData.first_name) + "</dd></div>");
    h.push('    <div class="input-row"><dt>生年月日</dt><dd>' + esc(userData.birth_year) + "年" + esc(userData.birth_month) + "月" + esc(userData.birth_day) + "日</dd></div>");
    h.push('    <div class="input-row"><dt>出生時刻</dt><dd>' + esc(labels.hour) + "</dd></div>");
    h.push('    <div class="input-row"><dt>性別</dt><dd>' + esc(labels.gender) + "</dd></div>");
    h.push('    <div class="input-row"><dt>出生地</dt><dd>' + esc(labels.prefecture) + "</dd></div>");
    h.push('    <div class="input-row"><dt>鑑定日</dt><dd>' + esc(formatDateJa(today)) + "</dd></div>");
    h.push("  </dl>");
    h.push('  <a class="submit-button link-button" href="' + indexHref() + '">もう一度占う</a>');
    h.push("</section>");

    document.title = userData.last_name + userData.first_name + "さんの今日の総合鑑定｜" +
      report.score_rank + "（" + report.total_score + "点）";
    return h.join("\n");
  }

  /* ------------------------------------------------------------------ */
  /* en/result.html（英語）— templates/en/result.html の描画を移植        */
  /* ------------------------------------------------------------------ */
  function renderResultEn(report, userData, today) {
    var labels = labelsEn(userData);
    var h = [];

    h.push('<section class="verdict" id="verdict">');
    h.push('  <p class="verdict-eyebrow">Today\'s Fortune for ' + esc(formatDateEn(today)) + "</p>");
    h.push('  <h1 class="verdict-name">' + esc(userData.last_name) + " " + esc(userData.first_name) + "</h1>");
    h.push('  <div class="verdict-main">');
    h.push('    <div class="rank-badge rank-' + esc(report.score_rank) + '">');
    h.push('      <span class="rank-label">Overall</span>');
    h.push('      <span class="rank-value">' + esc(report.score_rank_en) + "</span>");
    h.push("    </div>");
    h.push('    <div class="score-block">');
    h.push('      <div class="score-number">');
    h.push('        <span class="score-value">' + esc(report.total_score) + '</span><span class="score-unit">/ 100</span>');
    h.push("      </div>");
    h.push('      <div class="progress" role="img" aria-label="Overall score ' + esc(report.total_score) + ' out of 100">');
    h.push('        <div class="progress-bar" style="width: ' + esc(report.total_score) + '%"></div>');
    h.push("      </div>");
    h.push('      <p class="score-note">Calculated as a weighted average across ' + moduleCount(report) + " divination systems.</p>");
    h.push("    </div>");
    h.push("  </div>");

    h.push('  <div class="lucky-grid">');
    h.push('    <div class="lucky-item">');
    h.push('      <p class="lucky-label">Lucky Colour</p>');
    h.push('      <p class="lucky-value"><span class="color-chip" style="background: ' + esc(report.lucky_color_hex) + '"></span> ' + esc(report.lucky_color_en) + "</p>");
    h.push('      <p class="lucky-sub">' + esc(report.lucky_color_hex) + "</p>");
    h.push("    </div>");
    h.push('    <div class="lucky-item"><p class="lucky-label">Lucky Item</p><p class="lucky-value">' + esc(report.lucky_item_en) + "</p></div>");
    h.push('    <div class="lucky-item"><p class="lucky-label">Lucky Direction</p><p class="lucky-value">' + esc(report.lucky_dir_en) + "</p></div>");
    h.push('    <div class="lucky-item"><p class="lucky-label">Lucky Number</p><p class="lucky-value">' + esc(report.lucky_number) + "</p></div>");
    h.push("  </div>");

    h.push('  <div class="message-block">');
    h.push('    <h2 class="block-title">Today\'s Overall Advice</h2>');
    h.push('    <p class="overall-message">' + esc(report.overall_message_en) + "</p>");
    h.push("  </div>");

    h.push('  <div class="category-block">');
    h.push('    <h2 class="block-title">Fortune by Category</h2>');
    h.push('    <ul class="category-list">');
    ["Love", "Work", "Money", "Health"].forEach(function (key) {
      var value = report.category_scores_en[key];
      h.push('      <li class="category-row">');
      h.push('        <span class="category-name">' + key + "</span>");
      h.push('        <span class="category-bar"><span class="category-fill category-' + key.toLowerCase() + '" style="width: ' + esc(value) + '%"></span></span>');
      h.push('        <span class="category-value">' + esc(value) + "</span>");
      h.push("      </li>");
    });
    h.push("    </ul>");
    h.push("  </div>");

    h.push(shareBlockEn(report, today));

    h.push('  <p class="verdict-disclaimer">* This reading is provided for entertainment purposes only and does not carry any scientific validity claim.</p>');
    h.push("</section>");

    h.push("<!-- ADSENSE_SLOT -->");
    h.push('<div class="ad-container ad-result-1">Advertisement</div>');

    h.push('<section class="card chart-card">');
    h.push('  <h2 class="card-title">Scores across all 11 systems</h2>');
    h.push('  <div class="chart-wrap">');
    h.push('    <canvas id="scoreRadar" width="400" height="400" aria-label="Radar chart of scores across 11 divination systems" role="img"></canvas>');
    h.push("  </div>");
    h.push('  <ul class="score-fallback" hidden>');
    Object.keys(report.score_breakdown_en).forEach(function (name) {
      h.push("    <li>" + esc(name) + ": " + esc(report.score_breakdown_en[name]) + "/100</li>");
    });
    h.push("  </ul>");
    h.push("  " + scoreDataScript(report.score_breakdown_en));
    h.push("</section>");

    h.push('<section class="detail-section">');
    h.push('  <h2 class="section-title">See the individual readings</h2>');
    h.push('  <p class="section-note">Each tradition\'s own score, lucky elements, and full reading — tap to expand.</p>');
    h.push('  <div class="accordion">');
    (report.detail_results_en || []).forEach(function (item) {
      h.push('    <details class="accordion-item">');
      h.push('      <summary class="accordion-head">');
      h.push('        <span class="accordion-title">' + esc(item.name_en) + "</span>");
      h.push('        <span class="accordion-score">' + esc(item.score) + "/100</span>");
      h.push('        <span class="accordion-icon" aria-hidden="true"></span>');
      h.push("      </summary>");
      h.push('      <div class="accordion-body">');
      h.push('        <div class="item-meter"><span class="item-meter-fill" style="width: ' + esc(item.score) + '%"></span></div>');
      h.push('        <ul class="item-lucky">');
      h.push("          <li><span>Colour</span>" + esc(item.lucky_color_en) + "</li>");
      h.push("          <li><span>Item</span>" + esc(item.lucky_item_en) + "</li>");
      h.push("          <li><span>Direction</span>" + esc(item.lucky_dir_en) + "</li>");
      h.push("        </ul>");
      if (item.detail_en) {
        h.push('        <p class="item-detail">' + esc(item.detail_en) + "</p>");
      } else {
        h.push('        <p class="item-detail">The full reading from ' + esc(item.name_en) +
               " — including the reasoning behind today's score — is written in Japanese. " +
               'If you\'d like the complete text, enter your details on the <a href="../">Japanese version</a> of this page.</p>');
      }
      h.push("      </div>");
      h.push("    </details>");
    });
    h.push("  </div>");
    h.push("</section>");

    h.push("<!-- ADSENSE_SLOT -->");
    h.push('<div class="ad-container ad-result-2">Advertisement</div>');

    h.push('<section class="card input-card">');
    h.push('  <h2 class="card-title">Details used for this reading</h2>');
    h.push('  <dl class="input-list">');
    h.push('    <div class="input-row"><dt>Name</dt><dd>' + esc(userData.last_name) + " " + esc(userData.first_name) + "</dd></div>");
    h.push('    <div class="input-row"><dt>Date of birth</dt><dd>' + esc(userData.birth_year) + "-" + pad2(userData.birth_month) + "-" + pad2(userData.birth_day) + "</dd></div>");
    h.push('    <div class="input-row"><dt>Time of birth</dt><dd>' + esc(labels.hour) + "</dd></div>");
    h.push('    <div class="input-row"><dt>Gender</dt><dd>' + esc(labels.gender) + "</dd></div>");
    h.push('    <div class="input-row"><dt>Place of birth</dt><dd>' + esc(labels.prefecture) + "</dd></div>");
    h.push('    <div class="input-row"><dt>Reading date</dt><dd>' + esc(formatDateEn(today)) + "</dd></div>");
    h.push("  </dl>");
    h.push('  <a class="submit-button link-button" href="' + indexHref() + '">Get another reading</a>');
    h.push("</section>");

    document.title = userData.last_name + userData.first_name + "'s Today's Fortune | " +
      report.score_rank_en + " (" + report.total_score + "/100)";
    return h.join("\n");
  }

  /* ------------------------------------------------------------------ */
  /* result.html エントリポイント                                        */
  /* ------------------------------------------------------------------ */
  function initResult() {
    var root = document.getElementById("result-root");
    if (!root) {
      return;
    }
    var params = readParams();
    if (!params.present) {
      // 直接アクセスされた場合は入力フォームへ戻す（Flask 版 GET /result と同じ）
      window.location.replace(indexHref());
      return;
    }
    var U = window.Uranai;
    if (!U || typeof U.validate !== "function" || typeof U.buildReport !== "function") {
      showAlert(root.parentNode, TEXT.engineMissing);
      return;
    }
    var checked = U.validate(params.values, lang);
    if (!checked || checked.error || !checked.userData) {
      // 入力エラー：パラメータごと index.html へ差し戻し、そちらで同じ検証結果を表示する
      window.location.replace(indexHref() + "?" + params.raw.toString());
      return;
    }
    var userData = checked.userData;
    var today = toYMD(userData.today) || jstToday();
    var report;
    try {
      report = U.buildReport(userData, lang);
    } catch (e) {
      showAlert(root.parentNode, TEXT.reportFailed);
      return;
    }
    root.innerHTML = isEnglish ? renderResultEn(report, userData, today)
                               : renderResultJa(report, userData, today);
    root.addEventListener("click", function (ev) {
      var a = ev.target.closest("[data-share], .consult-button");
      if (!a || typeof window.gtag !== "function") return;
      window.gtag("event", a.dataset.share ? "share" : "consult_click", {
        method: a.dataset.share || "coconala",
        content_type: "reading",
        lang: lang
      });
    });
  }

  if (page === "index") {
    initIndex();
  } else if (page === "result") {
    initResult();
  }
})();
