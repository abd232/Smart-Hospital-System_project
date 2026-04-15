let currentSessionId = null;

function addMessage(text, sender) {
  const chatBox = document.getElementById("chatBox");

  const wrapper = document.createElement("div");
  wrapper.className =
    "mb-3 " + (sender === "user" ? "text-right" : "text-left");

  const bubble = document.createElement("div");
  bubble.className =
    sender === "user"
      ? "bg-blue-600 text-white p-3 rounded-xl inline-block max-w-[80%]"
      : "bg-blue-100 text-gray-800 p-3 rounded-xl inline-block max-w-[80%]";

  bubble.textContent = text;
  wrapper.appendChild(bubble);
  chatBox.appendChild(wrapper);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function renderDoctors(doctors, specialty) {
  const container = document.getElementById("doctorResults");

  if (!doctors || doctors.length === 0) {
    container.innerHTML = `
      <div class="col-span-3 text-center py-5">
        <h4>No doctors found.</h4>
      </div>
    `;
    container.classList.remove("hidden");
    return;
  }

  let html = `
    <div class="max-w-5xl mx-auto mt-8 mb-6">
      <div class="bg-green-50 border-l-4 border-green-500 p-4 rounded-xl shadow-md">
        <h3 class="font-bold text-green-700 text-lg mb-1">Suggested Doctors</h3>
        <p class="text-gray-700 text-sm">
          Recommended specialty: <span class="font-semibold">${specialty || "General Checkup"}</span>
        </p>
      </div>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 max-w-5xl mx-auto">
  `;

  doctors.forEach((doctor) => {
    const firstInitial = doctor.first_name
      ? doctor.first_name.charAt(0).toUpperCase()
      : "";
    const lastInitial = doctor.last_name
      ? doctor.last_name.charAt(0).toUpperCase()
      : "";

    html += `
      <div
        class="rounded-2xl border border-border bg-card p-6 hover:shadow-lg hover:border-primary/30 transition-all duration-300 text-center bg-white"
      >
        <div
          class="w-20 h-20 rounded-full bg-accent mx-auto mb-4 flex items-center justify-center first-name"
        >
          <span class="text-2xl font-bold text-primary">
            ${firstInitial}${lastInitial}
          </span>
        </div>

        <h3 class="font-bold text-foreground text-lg">
          Dr. ${doctor.first_name} ${doctor.last_name}
        </h3>

        <p class="text-primary text-sm font-medium mb-1">
          ${doctor.specialty || ""}
        </p>

        <p class="text-muted-foreground text-xs mb-1">
          ${doctor.clinic || ""}
        </p>

        <p class="text-muted-foreground text-xs mb-4">
          ${doctor.section || ""}
        </p>

        <button
          type="button"
          class="inline-flex items-center justify-center gap-2 whitespace-nowrap text-sm font-medium bg-primary text-primary-foreground hover:bg-primary/90 h-9 rounded-md px-3 w-full open-booking-modal"
          data-doctor-id="${doctor.id}"
          data-doctor-name="Dr. ${doctor.first_name} ${doctor.last_name}"
          data-doctor-specialty="${doctor.specialty || ""}"
          data-doctor-clinic="${doctor.clinic || ""}"
        >
          Book Appointment
        </button>
      </div>
    `;
  });

  html += `</div>`;

  container.innerHTML = html;
  container.classList.remove("hidden");
}

async function sendMessage() {
  const input = document.getElementById("symptoms");
  const sendBtn = document.getElementById("sendBtn");
  const text = input.value.trim();

  if (!text) return;

  addMessage(text, "user");
  input.value = "";
  sendBtn.disabled = true;
  sendBtn.textContent = "Sending...";

  try {
    const response = await fetch("/ai/chat/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({
        message: text,
        session_id: currentSessionId,
      }),
    });

    const data = await response.json();

    if (data.error) {
      addMessage(data.error, "assistant");
      return;
    }

    currentSessionId = data.session_id;
    addMessage(data.assistant_reply, "assistant");

    if (data.enough_information) {
      renderDoctors(data.doctors, data.recommended_specialty);
    }
  } catch (error) {
    addMessage("Something went wrong. Please try again.", "assistant");
    console.error(error);
  } finally {
    sendBtn.disabled = false;
    sendBtn.textContent = "Send";
  }
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
