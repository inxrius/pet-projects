// Конфигурация
const STORAGE_KEY = 'crm_leads';

// Тексты для отображения
const sourceLabels = {
    'cold': 'Холодный',
    'warm': 'Тёплый'
};

const responsibleLabels = {
    'lidorub': 'Лидоруб',
    'mop': 'МОП'
};

const stageLabels = {
    'new': 'Новый лид',
    'qualified': 'Квалифицирован',
    'consultation': 'Назначена консультация',
    'rejection': 'Отказ'
};

// Загрузка лидов из localStorage
function loadLeads() {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored ? JSON.parse(stored) : [];
}

// Сохранение лидов в localStorage
function saveLeads(leads) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(leads));
}

// Валидация формы
function validateForm(name, phone) {
    const errors = [];
    
    if (!name || name.trim() === '') {
        errors.push('Имя клиента обязательно для заполнения');
    }
    
    if (!phone || phone.trim() === '') {
        errors.push('Номер телефона обязателен для заполнения');
    }
    
    return errors;
}

// Показать ошибку
function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    errorDiv.classList.add('show');
    
    setTimeout(() => {
        errorDiv.classList.remove('show');
    }, 5000);
}

// Создать карточку лида
function createLeadCard(lead) {
    const card = document.createElement('div');
    card.className = 'lead-card';
    card.dataset.leadId = lead.id;
    
    const sourceClass = lead.source === 'cold' ? 'badge-cold' : 'badge-warm';
    const stageClass = `badge-${lead.stage}`;
    
    card.innerHTML = `
        <div class="lead-header">
            <div>
                <div class="lead-name">${escapeHtml(lead.name)}</div>
                <div class="lead-phone">${escapeHtml(lead.phone)}</div>
            </div>
            <span class="badge ${sourceClass}">${sourceLabels[lead.source]}</span>
        </div>
        <div class="lead-details">
            <div class="lead-detail">
                <span class="lead-detail-label">Ответственный</span>
                <span class="lead-detail-value">${responsibleLabels[lead.responsible]}</span>
            </div>
            <div class="lead-detail">
                <span class="lead-detail-label">Этап сделки</span>
                <span class="lead-detail-value">
                    <span class="badge ${stageClass}">${stageLabels[lead.stage]}</span>
                </span>
            </div>
            <div class="lead-detail">
                <span class="lead-detail-label">Запрошено ТЗ</span>
                <span class="lead-detail-value">${lead.techSpec ? 'Да' : 'Нет'}</span>
            </div>
            <div class="lead-detail">
                <span class="lead-detail-label">Дата создания</span>
                <span class="lead-detail-value">${new Date(lead.createdAt).toLocaleString('ru-RU')}</span>
            </div>
        </div>
        <div class="lead-actions">
            <label for="stage-${lead.id}" style="font-size: 13px; color: #666; margin-right: 10px;">Изменить этап:</label>
            <select class="stage-select" id="stage-${lead.id}" onchange="updateLeadStage('${lead.id}', this.value)">
                <option value="new" ${lead.stage === 'new' ? 'selected' : ''}>Новый лид</option>
                <option value="qualified" ${lead.stage === 'qualified' ? 'selected' : ''}>Квалифицирован</option>
                <option value="consultation" ${lead.stage === 'consultation' ? 'selected' : ''}>Назначена консультация</option>
                <option value="rejection" ${lead.stage === 'rejection' ? 'selected' : ''}>Отказ</option>
            </select>
        </div>
    `;
    
    return card;
}

// Экранирование HTML для безопасности
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Отображение всех лидов
function displayLeads() {
    const leadsList = document.getElementById('leadsList');
    const leads = loadLeads();
    
    leadsList.innerHTML = '';
    
    if (leads.length === 0) {
        leadsList.innerHTML = '<div class="empty-state">Пока нет сохранённых лидов</div>';
        return;
    }
    
    // Сортируем по дате создания (новые сверху)
    leads.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
    
    leads.forEach(lead => {
        const card = createLeadCard(lead);
        leadsList.appendChild(card);
    });
}

// Обновление этапа сделки
function updateLeadStage(leadId, newStage) {
    const leads = loadLeads();
    const leadIndex = leads.findIndex(l => l.id === leadId);
    
    if (leadIndex !== -1) {
        leads[leadIndex].stage = newStage;
        saveLeads(leads);
        
        // Обновляем отображение
        displayLeads();
        
        // Показываем уведомление
        showError(`Этап сделки обновлён на: ${stageLabels[newStage]}`);
    }
}

// Обработка отправки формы
function handleFormSubmit(event) {
    event.preventDefault();
    
    // Получаем данные из формы
    const name = document.getElementById('clientName').value;
    const phone = document.getElementById('phone').value;
    const source = document.getElementById('leadSource').value;
    const responsible = document.getElementById('responsible').value;
    const stage = document.getElementById('dealStage').value;
    const techSpec = document.getElementById('techSpec').checked;
    
    // Валидация
    const errors = validateForm(name, phone);
    
    if (errors.length > 0) {
        showError(errors.join('. '));
        return;
    }
    
    // Создаём нового лида
    const newLead = {
        id: Date.now().toString(), // Уникальный ID на основе времени
        name: name.trim(),
        phone: phone.trim(),
        source: source,
        responsible: responsible,
        stage: stage,
        techSpec: techSpec,
        createdAt: new Date().toISOString()
    };
    
    // Загружаем существующие лиды и добавляем нового
    const leads = loadLeads();
    leads.push(newLead);
    
    // Сохраняем в localStorage
    saveLeads(leads);
    
    // Очищаем форму
    document.getElementById('leadForm').reset();
    
    // Обновляем отображение
    displayLeads();
    
    // Показываем успешное сообщение
    showError('Лид успешно сохранён!');
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Отображаем существующие лиды
    displayLeads();
    
    // Добавляем обработчик формы
    document.getElementById('leadForm').addEventListener('submit', handleFormSubmit);
});

// Дополнительное задание: пример API-запроса
// Функция для отправки данных на сервер (демонстрация)
async function sendLeadToAPI(lead) {
    const API_URL = 'https://api.example.com/leads'; // Пример URL
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(lead)
        });
        
        if (response.ok) {
            console.log('Лид успешно отправлен на сервер');
        } else {
            console.error('Ошибка отправки на сервер');
        }
    } catch (error) {
        console.error('Ошибка сети:', error);
    }
}

// Примечание: Для использования API-запроса раскомментируйте строку ниже в handleFormSubmit:
// await sendLeadToAPI(newLead);