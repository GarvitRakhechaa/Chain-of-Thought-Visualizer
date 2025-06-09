
async function sendQuery() {
  const input = document.getElementById("userInput").value.trim();
  const messagesDiv = document.getElementById("messages");
  if (!input) return;

    messagesDiv.innerHTML = `<p class="loader">Thinking... 🔄</p>`;

      try {
        const res = await fetch("http://localhost:8000/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ input_str: input }),
        });

        const data = await res.json();
        const assistantSteps = [];

        data.messages.forEach(msg => {
          if (msg.role === "assistant") {
            try {
              const parsed = JSON.parse(msg.content);
              if (parsed.step && parsed.content) {
                assistantSteps.push(parsed);
              }
            } catch (err) {
              // Skip invalid JSON
            }
          }
        });

        if (assistantSteps.length === 0) {
          messagesDiv.innerHTML = `<p style="color: orange;">No valid response received.</p>`;
          return;
        }

        // Clear messagesDiv before showing steps
        messagesDiv.innerHTML = "";

        let index = 0;

        function showNextStep() {
          if (index >= assistantSteps.length) return;

          const step = assistantSteps[index];
          const div = document.createElement("div");
          div.classList.add("step");
          div.innerHTML = `<strong>${step.step.toUpperCase()}</strong>${step.content}`;
          messagesDiv.appendChild(div);

          // Animate visibility
          setTimeout(() => {
            div.classList.add("visible");
          }, 50);

          index++;
          // Show next step after 3.5 seconds
          setTimeout(showNextStep, 3500);
        }

        showNextStep();

      } catch (err) {
        messagesDiv.innerHTML = `<p style="color: red;">❌ Error: ${err.message}</p>`;
      }
    }