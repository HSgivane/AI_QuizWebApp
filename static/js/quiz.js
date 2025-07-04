function showAnswer(btn, selected, correct) {
    const index = btn.dataset.index;
    const block = btn.parentElement;
    const buttons = block.querySelectorAll('.answer-btn');
    const input = document.getElementById(`q${index}`);

    if (input) {
        input.value = selected;
    } else {
        console.error("Input not found for index:", index);
    }

    buttons.forEach(b => b.disabled = true);

    if (selected === correct) {
        btn.classList.add("correct");
    } else {
        btn.classList.add("wrong");
        buttons.forEach(b => {
            if (b.textContent.trim().startsWith(correct + ")")) {
                b.classList.add("correct");
            }
        });
    }

    console.log(`Ответ [${index}]: выбран ${selected}, правильный ${correct}`);
}
