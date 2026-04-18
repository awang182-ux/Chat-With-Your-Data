/**
 * Chat with Your Data — form handler.
 * POSTs FormData (question + file) to the Flask /analyze route.
 */
(function () {
  var ANALYZE_URL = "/analyze";

  var form = document.getElementById("analyze-form");
  var submitBtn = document.getElementById("submit-btn");
  var btnText = document.getElementById("btn-text");
  var loadingHint = document.getElementById("loading-hint");
  var results = document.getElementById("results");
  var questionArea = document.getElementById("question-area");
  var questionDisplay = document.getElementById("question-display");
  var errorArea = document.getElementById("error-area");
  var errorText = document.getElementById("error-text");
  var resultArea = document.getElementById("result-area");
  var finalResultEl = document.getElementById("final-result");
  var codeArea = document.getElementById("code-area");
  var generatedCodeEl = document.getElementById("generated-code");

  function setLoading(isLoading) {
    submitBtn.disabled = isLoading;
    submitBtn.classList.toggle("is-loading", isLoading);
    loadingHint.classList.toggle("hidden", !isLoading);
    btnText.textContent = isLoading ? "Analyzing…" : "Analyze";

    var fileInput = document.getElementById("file");
    var questionInput = document.getElementById("question");
    fileInput.disabled = isLoading;
    questionInput.disabled = isLoading;

    var chips = document.querySelectorAll(".example-chip");
    for (var i = 0; i < chips.length; i++) {
      chips[i].disabled = isLoading;
    }
  }

  function hideResults() {
    results.classList.add("hidden");
    questionArea.classList.add("hidden");
    errorArea.classList.add("hidden");
    resultArea.classList.add("hidden");
    codeArea.classList.add("hidden");
    questionDisplay.textContent = "";
    errorText.textContent = "";
    finalResultEl.textContent = "";
    generatedCodeEl.textContent = "";
  }

  function showJsonInPre(element, data) {
    if (data === undefined || data === null) {
      element.textContent = String(data);
      return;
    }
    if (typeof data === "object") {
      element.textContent = JSON.stringify(data, null, 2);
    } else {
      element.textContent = String(data);
    }
  }

  // Example questions: fill the input when a chip is clicked.
  document.querySelectorAll(".example-chip").forEach(function (chip) {
    chip.addEventListener("click", function () {
      var q = chip.getAttribute("data-question");
      if (q) {
        document.getElementById("question").value = q;
        document.getElementById("question").focus();
      }
    });
  });

  form.addEventListener("submit", async function (event) {
    event.preventDefault();

    var questionInput = document.getElementById("question");
    var fileInput = document.getElementById("file");

    var question = questionInput.value.trim();
    var file = fileInput.files[0];

    if (!question) {
      alert("Please enter a question.");
      return;
    }
    if (!file) {
      alert("Please choose a CSV file.");
      return;
    }

    var formData = new FormData();
    formData.append("question", question);
    formData.append("file", file);

    hideResults();
    setLoading(true);

    try {
      var response = await fetch(ANALYZE_URL, {
        method: "POST",
        body: formData,
      });

      var data = await response.json().catch(function () {
        return { success: false, error: "Invalid JSON response from server." };
      });

      results.classList.remove("hidden");
      questionArea.classList.remove("hidden");
      questionDisplay.textContent =
        data.question && String(data.question).trim()
          ? data.question
          : question;

      if (!response.ok || data.success === false) {
        errorArea.classList.remove("hidden");
        errorText.textContent =
          data.error || "Request failed (HTTP " + response.status + ").";
        return;
      }

      if (data.error) {
        errorArea.classList.remove("hidden");
        errorText.textContent = data.error;
      }

      resultArea.classList.remove("hidden");
      showJsonInPre(finalResultEl, data.final_result);

      if (data.generated_code !== undefined && data.generated_code !== null) {
        codeArea.classList.remove("hidden");
        generatedCodeEl.textContent = String(data.generated_code);
      }
    } catch (err) {
      results.classList.remove("hidden");
      questionArea.classList.remove("hidden");
      questionDisplay.textContent = question;

      errorArea.classList.remove("hidden");
      errorText.textContent =
        "Network error: " +
        (err && err.message ? err.message : String(err)) +
        ". Is the Flask server running?";
    } finally {
      setLoading(false);
    }
  });
})();
