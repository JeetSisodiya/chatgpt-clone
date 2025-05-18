// Example POST method implementation:
async function postData(url = "", data = {}) { 
    const response = await fetch(url, {
      method: "POST", headers: {
        "Content-Type": "application/json", 
      }, body: JSON.stringify(data),  
    });
    return response.json(); 
  }

  sendButton.addEventListener("click", async ()=>{ 
    questionInput = document.getElementById("questionInput").value;
    document.getElementById("questionInput").value = "";
    document.querySelector(".right2").style.display = "block"
    document.querySelector(".right1").style.display = "none"

    question1.innerHTML = questionInput;
    question2.innerHTML = questionInput;

    // Get the answer and populate it! 
    let result = await postData("/api", {"question": questionInput})
    solution.innerHTML = result.answer
})
//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
//sk-proj-7gRRZ3Jqfu3Y1dfzl0wXRgSCzLqdrodDh89h3-BpWPY3uNl3vLQFE1Ybp-uykK3MEKnaJ8A4qPT3BlbkFJU9SYVaQL7KRuq9zOcYmW7LtOCUgliZtK0T8e927UP-SOc8TbXWvqkqJNc4MA