import * as monaco from 'monaco-editor';

// Initialize editor with default settings
function initEditor() {
    const editor = monaco.editor.create(document.getElementById('editor'), {
        value: `function example() {
    console.log("Hello World");
}`,
        language: 'javascript',
        theme: 'vs-dark',
        minimap: { enabled: false },
        automaticLayout: true,
        fontSize: 14,
        lineNumbers: 'on',
        scrollBeyondLastLine: false,
        roundedSelection: false,
        padding: {
            top: 10,
            bottom: 10
        }
    });

    // Handle window resizing
    window.addEventListener('resize', () => {
        editor.layout();
    });

    return editor;
}

// Export the editor instance for potential external use
export const editor = initEditor(); 