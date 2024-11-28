const CONFIG = {
  API_URL: " https://toeic-grades-query-85f602b6b682.herokuapp.com/", // 開發環境
};

class ScoreQuerySystem {
  constructor() {
    this.apiUrl = CONFIG.API_URL;
    this.form = document.getElementById("queryForm");
    this.loadingDiv = document.getElementById("loading");
    this.resultDiv = document.getElementById("result");
    this.initializeEventListeners();
  }

  initializeEventListeners() {
    this.form.addEventListener("submit", (e) => this.handleSubmit(e));
  }

  async handleSubmit(e) {
    e.preventDefault();
    const studentId = document.getElementById("student_id").value;

    try {
      this.showLoading();
      const response = await this.queryScore(studentId);

      if (response.success) {
        this.showScoresWithAnimation(response.data);
      } else {
        this.showError(response.message);
      }
    } catch (error) {
      this.showError("查詢失敗，請稍後再試");
      console.error("Error:", error);
    } finally {
      this.hideLoading();
    }
  }

  async queryScore(studentId) {
    const response = await fetch(`${this.apiUrl}/api/query`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
      body: JSON.stringify({ student_id: studentId }),
    });

    return await response.json();
  }

  showScoresWithAnimation(data) {
    this.resultDiv.classList.remove("d-none");
    const elements = {
      listening: document.getElementById("listening_score"),
      reading: document.getElementById("reading_score"),
      total: document.getElementById("total_score"),
    };

    Object.entries(elements).forEach(([key, element]) => {
      const targetScore = data[`${key}_score`];
      this.animateNumber(element, targetScore);
    });
  }

  animateNumber(element, target) {
    const duration = 1000;
    const steps = 60;
    const step = target / steps;
    let current = 0;
    const interval = duration / steps;

    const timer = setInterval(() => {
      current += step;
      if (current >= target) {
        clearInterval(timer);
        element.textContent = target;
      } else {
        element.textContent = Math.floor(current);
      }
    }, interval);
  }

  showError(message) {
    const alert = document.createElement("div");
    alert.className = "alert alert-danger alert-dismissible fade show mt-3";
    alert.innerHTML = `
          ${message}
          <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      `;
    document.querySelector(".card-body").insertBefore(alert, this.resultDiv);
  }

  showLoading() {
    this.loadingDiv.classList.remove("d-none");
    this.resultDiv.classList.add("d-none");
  }

  hideLoading() {
    this.loadingDiv.classList.add("d-none");
  }
}

// 初始化應用
document.addEventListener("DOMContentLoaded", () => {
  new ScoreQuerySystem();
});
