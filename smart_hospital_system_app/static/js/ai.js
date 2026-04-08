function getRecommendation() {
  const symptoms = document.getElementById("symptoms").value.trim();
  const result = document.getElementById("result");
  const resultText = document.getElementById("resultText");

  if (!symptoms) {
    resultText.textContent = "Please describe your symptoms first.";
    result.classList.remove("hidden");
    result.classList.add("fade-in");
    return;
  }

  // Example simple AI logic (replace with real AI logic)
  let recommendation = "General Checkup";

  if (symptoms.toLowerCase().includes("chest")) recommendation = "Cardiology";
  else if (symptoms.toLowerCase().includes("skin"))
    recommendation = "Dermatology";
  else if (symptoms.toLowerCase().includes("eye"))
    recommendation = "Ophthalmology";
  else if (symptoms.toLowerCase().includes("stomach"))
    recommendation = "Gastroenterology";

  resultText.textContent = `Recommended Department: ${recommendation}`;
  result.classList.remove("hidden");
  result.classList.add("fade-in");
}
