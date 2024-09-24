data = {
}

  function addItemsToList(element, parentUl, indentLevel) {
    const li = document.createElement('li');
    li.textContent = element.name;
    li.classList.add(`pl-[${indentLevel * 2}px]`, 'cursor-pointer', 'text-blue-500'); // Стиль курсора и цвет текста
    li.dataset.indentLevel = indentLevel; // Сохраняем уровень вложенности в атрибуте data

    // Создаем вложенный ul для дочерних элементов
    const ul = document.createElement('ul');
    ul.classList.add('list-none', 'hidden'); // Скрываем дочерний список по умолчанию
    li.appendChild(ul);

    // Добавляем элемент <li> в родительский <ul>
    parentUl.appendChild(li);

    if (element.type === "dir") {
      // Добавляем обработчик клика для сворачивания/разворачивания
      li.addEventListener('click', (event) => {
        if (!getSelection().isCollapsed) return;
        // Проверяем, если клик был не на элементе файла
        if (event.target.tagName !== 'LI' || element.type !== 'file') {
          event.stopPropagation(); // Останавливаем распространение события
          ul.classList.toggle('hidden'); // Переключаем класс hidden для показа/скрытия
        }
      });

      // Обрабатываем дочерние элементы директории
      if (element.child && element.child.length > 0) {
        element.child.forEach(child => {
          addItemsToList(child, ul, indentLevel + 1);
        });
      }
    } else if (element.type === "file") {
      // Для файлов просто добавляем их в родительский <ul>
      li.classList.remove('cursor-pointer', 'text-blue-500'); // Убираем курсор и цвет текста для файлов
      li.classList.add('text-gray-500'); // Устанавливаем цвет текста для файлов

      // Добавляем обработчик клика, чтобы предотвратить открытие родительского ul
      li.addEventListener('click', (event) => {
        event.stopImmediatePropagation(); // Останавливаем все события клика
      });

      parentUl.appendChild(li);
    }
  }
const rootUl = document.querySelector('.root');
addItemsToList(data, rootUl, 0);


function logEvent(event) {
    console.log(`Event: ${event.type}, Target: ${event.target.tagName}, Time: ${new Date()}`);
}

// Перечень событий, которые вы хотите отслеживать
const events = [
    'click',
    'dblclick',
    'keydown',
    'keyup',
    'mouseout',
    'focus',
    'blur'
];

// Добавляем обработчик для каждого события
events.forEach(eventType => {
    document.addEventListener(eventType, logEvent);
});
// console.log(rootUl)