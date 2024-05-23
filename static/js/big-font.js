function increaseFontSize(multiplier) {
    const elements = document.querySelectorAll('a, h1, h2, h3, h4, h5, h6, th, p, input, textarea, span, li, label');
    console.log(elements);
    elements.forEach(element => {
        // Получаем текущий размер шрифта
        const style = window.getComputedStyle(element);
        const currentFontSize = parseFloat(style.fontSize);
        if (currentFontSize) {
            element.style.fontSize = (currentFontSize * multiplier) + 'px';
        }
    });
}

increaseFontSize(2);
