const API_BASE_URL = 'http://localhost:8000';

let tools = [];
let selectedCategory = 'All';
let currentTool = null;

// DOM Elements
const categoryContainer = document.getElementById('category-container');
const toolsGrid = document.getElementById('tools-grid');
const toolModal = document.getElementById('tool-modal');
const closeModalBtn = document.getElementById('close-modal');
const processBtn = document.getElementById('process-btn');

// Modal Elements
const modalTitle = document.getElementById('modal-title');
const modalCategory = document.getElementById('modal-category');
const modalDescription = document.getElementById('modal-description');
const modalUseCase = document.getElementById('modal-usecase');
const modalCapabilities = document.getElementById('modal-capabilities');
const modalLimitations = document.getElementById('modal-limitations');
const modalInputType = document.getElementById('modal-input-type');
const textInputGroup = document.getElementById('text-input-group');
const fileInputGroup = document.getElementById('file-input-group');
const textInput = document.getElementById('text-input');
const fileInput = document.getElementById('file-input');
const resultBox = document.getElementById('result-box');
const resultType = document.getElementById('result-type');
const resultTime = document.getElementById('result-time');
const resultMessage = document.getElementById('result-message');
const resultInputInfo = document.getElementById('result-input-info');
const resultContent = document.getElementById('result-content');
const resultSettings = document.getElementById('result-settings');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    fetchTools();

    closeModalBtn.addEventListener('click', closeModal);
    toolModal.addEventListener('click', (e) => {
        if (e.target === toolModal) closeModal();
    });

    processBtn.addEventListener('click', processTool);
});

async function fetchTools() {
    try {
        const response = await fetch(`${API_BASE_URL}/tools`);
        tools = await response.json();
        renderCategories();
        renderTools();
    } catch (error) {
        console.error('Error fetching tools:', error);
        toolsGrid.innerHTML = '<p>Failed to load tools. Please ensure the backend is running.</p>';
    }
}

function renderCategories() {
    const categories = ['All', ...new Set(tools.map(t => t.category).filter(Boolean))];

    categoryContainer.innerHTML = categories.map(cat => `
        <button class="category-btn ${cat === selectedCategory ? 'active' : ''}"
                onclick="setCategory('${cat}')">
            ${cat}
        </button>
    `).join('');
}

window.setCategory = (cat) => {
    selectedCategory = cat;
    renderCategories();
    renderTools();
};

function renderTools() {
    const filteredTools = selectedCategory === 'All'
        ? tools
        : tools.filter(t => t.category === selectedCategory);

    toolsGrid.innerHTML = filteredTools.map(tool => `
        <div class="card" onclick="openTool('${tool.tool_name}')">
            <h3>${tool.tool_name}</h3>
            <div class="tags">
                <span class="tag">${tool.category}</span>
            </div>
            <p>${tool.description}</p>
        </div>
    `).join('');
}

window.openTool = (toolName) => {
    currentTool = tools.find(t => t.tool_name === toolName);
    if (!currentTool) return;

    modalTitle.textContent = currentTool.tool_name;
    modalCategory.textContent = currentTool.category;
    modalDescription.textContent = currentTool.description;
    modalUseCase.textContent = currentTool.use_case;

    // Capabilities
    modalCapabilities.innerHTML = (currentTool.capabilities || [])
        .map(c => `<span class="tag">${c}</span>`).join('');

    // Limitations
    modalLimitations.innerHTML = (currentTool.limitations || [])
        .map(c => `<span class="tag" style="background: #fee; color: #622; border-color: #edd">${c}</span>`).join('');

    modalInputType.textContent = currentTool.input_type;

    // Reset Inputs
    textInput.value = '';
    fileInput.value = '';
    resultBox.style.display = 'none';

    // Determine Input UI
    const inputType = currentTool.input_type.toLowerCase();
    const toolNameLower = currentTool.tool_name.toLowerCase();

    const showText = inputType.includes('text') ||
                     inputType.includes('url') ||
                     inputType === 'any' ||
                     toolNameLower.includes('text') ||
                     toolNameLower.includes('qr');

    const showFile = !showText || inputType.includes('/');

    textInputGroup.style.display = showText ? 'block' : 'none';
    fileInputGroup.style.display = showFile ? 'block' : 'none';

    toolModal.style.display = 'flex';
};

function closeModal() {
    toolModal.style.display = 'none';
    currentTool = null;
}

async function processTool() {
    if (!currentTool) return;

    processBtn.disabled = true;
    processBtn.textContent = 'Processing...';
    resultBox.style.display = 'none';

    const formData = new FormData();

    if (textInputGroup.style.display !== 'none' && textInput.value) {
        formData.append('text_input', textInput.value);
    }

    if (fileInputGroup.style.display !== 'none' && fileInput.files[0]) {
        formData.append('file', fileInput.files[0]);
    }

    try {
        const response = await fetch(`${API_BASE_URL}/process/${currentTool.tool_name}`, {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        renderResult(result);

    } catch (error) {
        console.error('Processing error:', error);
        renderResult({
            status: 'error',
            message: 'Network error or backend unreachable.',
            processing_time_ms: 0
        });
    } finally {
        processBtn.disabled = false;
        processBtn.textContent = 'Process';
    }
}

function renderResult(result) {
    resultBox.style.display = 'block';
    resultBox.className = `result-box ${result.status}`;

    resultType.textContent = result.output_type || 'Unknown';
    resultTime.textContent = result.processing_time_ms ? `${result.processing_time_ms}ms` : '';
    resultMessage.textContent = result.message || '';
    resultInputInfo.textContent = result.input_received ? `Input: ${result.input_received}` : '';

    resultContent.innerHTML = '';

    if (result.status === 'success' && result.output_data) {
        if (typeof result.output_data === 'string') {
             if (result.output_data.startsWith('http')) {
                // Download Link or Image
                const isImage = result.output_data.match(/\.(jpeg|jpg|gif|png)$/i) ||
                                (result.output_type && result.output_type.toLowerCase().includes('image'));

                if (isImage) {
                    resultContent.innerHTML = `<img src="${result.output_data}" alt="Output" style="max-width: 100%; max-height: 300px;">`;
                } else {
                    resultContent.innerHTML = `<a href="${result.output_data}" download class="process-btn" style="display: inline-block; text-decoration: none; text-align: center;">Download Result</a>`;
                }
             } else if (result.output_data.startsWith('data:image')) {
                 resultContent.innerHTML = `<img src="${result.output_data}" alt="Output" style="max-width: 100%; max-height: 300px;">`;
             } else {
                 resultContent.textContent = result.output_data;
             }
        } else {
            resultContent.textContent = JSON.stringify(result.output_data, null, 2);
        }
    }

    if (result.settings_used) {
        resultSettings.textContent = `Settings Used: ${JSON.stringify(result.settings_used)}`;
    } else {
        resultSettings.textContent = '';
    }
}
