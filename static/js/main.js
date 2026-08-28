/* =========================================================================
 * 今日の総合鑑定 — フロントエンドスクリプト
 *  1. フォーム送信時のローディング表示（Render無料プランのスリープ対策）
 *  2. 初回アクセス時のウォームアップ表示
 *  3. 11種スコアのレーダーチャート描画（Chart.js）
 *  4. アコーディオンの開閉補助
 * ========================================================================= */
(function () {
  "use strict";

  /* ------------------------------------------------------------------ */
  /* 1. ローディングオーバーレイ                                          */
  /* ------------------------------------------------------------------ */
  var overlay = document.getElementById("loading-overlay");

  function showLoading(message) {
    if (!overlay) {
      return;
    }
    if (message) {
      var text = overlay.querySelector(".loading-text");
      if (text) {
        text.textContent = message;
      }
    }
    overlay.hidden = false;
  }

  function hideLoading() {
    if (overlay) {
      overlay.hidden = true;
    }
  }

  // フォーム送信時にローディングを表示する
  var form = document.getElementById("uranai-form");
  if (form) {
    form.addEventListener("submit", function () {
      var button = form.querySelector(".submit-button");
      if (button) {
        button.disabled = true;
        button.textContent = "鑑定中……";
      }
      showLoading("十一の暦を照らし合わせています……");
    });
  }

  // ブラウザバックで戻ってきたときにローディングが残らないようにする
  window.addEventListener("pageshow", function (event) {
    if (event.persisted) {
      hideLoading();
      if (form) {
        var button = form.querySelector(".submit-button");
        if (button) {
          button.disabled = false;
          button.textContent = "今日の総合鑑定を見る";
        }
      }
    }
  });

  /* ------------------------------------------------------------------ */
  /* 2. 初回アクセス時のウォームアップ表示                                */
  /*    Render無料プランはアイドル後の初回リクエストに時間がかかるため、    */
  /*    ページ描画が遅れている間だけインジケータを出す。                   */
  /* ------------------------------------------------------------------ */
  if (document.readyState === "loading") {
    var warmupTimer = window.setTimeout(function () {
      showLoading("サーバーを起動しています……");
    }, 1200);
    window.addEventListener("DOMContentLoaded", function () {
      window.clearTimeout(warmupTimer);
      hideLoading();
    });
  }

  /* ------------------------------------------------------------------ */
  /* 3. レーダーチャート                                                 */
  /* ------------------------------------------------------------------ */
  function initScoreRadar() {
    var canvas = document.getElementById("scoreRadar");
    var dataNode = document.getElementById("score-data");
    if (!canvas || !dataNode || typeof window.Chart === "undefined") {
      return;
    }

    var scores;
    try {
      scores = JSON.parse(dataNode.textContent);
    } catch (e) {
      return;
    }

    var labels = Object.keys(scores);
    var values = labels.map(function (key) {
      return scores[key];
    });

    new window.Chart(canvas.getContext("2d"), {
      type: "radar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "今日のスコア",
            data: values,
            fill: true,
            backgroundColor: "rgba(158, 27, 50, 0.18)",
            borderColor: "rgba(158, 27, 50, 0.85)",
            borderWidth: 2,
            pointBackgroundColor: "rgba(201, 162, 39, 1)",
            pointBorderColor: "rgba(20, 32, 63, 1)",
            pointRadius: 3,
            pointHoverRadius: 5
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        aspectRatio: 1,
        animation: { duration: 700 },
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: function (context) {
                return context.label + "：" + context.formattedValue + "点";
              }
            }
          }
        },
        scales: {
          r: {
            min: 0,
            max: 100,
            ticks: {
              stepSize: 25,
              backdropColor: "rgba(0, 0, 0, 0)",
              color: "#8a8f98",
              font: { size: 10 }
            },
            grid: { color: "rgba(20, 32, 63, 0.12)" },
            angleLines: { color: "rgba(20, 32, 63, 0.12)" },
            pointLabels: {
              color: "#14203f",
              font: { size: 11 }
            }
          }
        }
      }
    });
  }

  /* ------------------------------------------------------------------ */
  /* 4. アコーディオン（1つ開いたら他を閉じる）                           */
  /* ------------------------------------------------------------------ */
  function initAccordion() {
    var items = document.querySelectorAll(".accordion > .accordion-item");
    Array.prototype.forEach.call(items, function (item) {
      item.addEventListener("toggle", function () {
        if (!item.open) {
          return;
        }
        Array.prototype.forEach.call(items, function (other) {
          if (other !== item) {
            other.open = false;
          }
        });
      });
    });
  }

  /* ------------------------------------------------------------------ */
  function init() {
    initScoreRadar();
    initAccordion();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
