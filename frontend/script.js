document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generate-btn');
    const apiKeyInput = document.getElementById('api-key');
    const promptInput = document.getElementById('prompt');
    const imagePlaceholder = document.getElementById('image-placeholder');

    console.log("AI Image Studio - MVP script loaded and ready.");

    generateBtn.addEventListener('click', async () => {
        const apiKey = apiKeyInput.value.trim();
        const prompt = promptInput.value.trim();

        if (!apiKey || !prompt) {
            alert('Por favor, preencha a API Key e o Prompt.');
            return;
        }

        // Atualiza a UI para indicar que o processo começou
        imagePlaceholder.innerHTML = '<p>Gerando imagem, por favor aguarde...</p>';
        generateBtn.disabled = true;
        generateBtn.textContent = 'Gerando...';

        try {
            // O backend está rodando na porta 5001
            const response = await fetch('http://127.0.0.1:5001/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    api_key: apiKey,
                    prompt: prompt,
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                // Se a resposta não for 2xx, lança um erro com a mensagem do backend
                throw new Error(data.error || 'Ocorreu um erro desconhecido.');
            }

            // Sucesso: exibe a imagem
            imagePlaceholder.innerHTML = `<img src="${data.image_url}" alt="Imagem gerada para: ${prompt}">`;

        } catch (error) {
            // Falha: exibe a mensagem de erro
            console.error('Erro ao gerar imagem:', error);
            imagePlaceholder.innerHTML = `<p style="color: red;">Erro: ${error.message}</p>`;
        } finally {
            // Reabilita o botão
            generateBtn.disabled = false;
            generateBtn.textContent = 'Gerar Imagem';
        }
    });
});