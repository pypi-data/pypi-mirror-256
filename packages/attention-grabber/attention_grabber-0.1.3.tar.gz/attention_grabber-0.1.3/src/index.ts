import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { NotebookActions, INotebookTracker } from '@jupyterlab/notebook';

/**
 * Initialization data for the attention-grabber extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'attention-grabber:plugin',
  description: 'Flashes your screen when cells are finished, until you click on the notebook again.',
  autoStart: true,
  requires: [INotebookTracker],
  activate: (app: JupyterFrontEnd, notebookTracker: INotebookTracker) => {
    console.log('JupyterLab extension attention-grabber is activated!');

    // Audio context for playing tone
    const audioContext = new AudioContext();

    // State management variables
    let annoyingInterval: number | null = null;
    let grabAttentionTimeout: number | null = null;
    let isPlaying = false;
    let oscillator: OscillatorNode | null = null;
    let extensionEnabled = false;

    // Function to start the attention-grabbing effect
    function grabAttention() {
      isPlaying = true;
      annoyingInterval = window.setInterval(toggleAnnoying, 500); // Toggle effect every 500ms
    }

    // Function to stop the effect and clear timeouts/intervals
    function stopAnnoying() {
      if (grabAttentionTimeout !== null) {
        clearTimeout(grabAttentionTimeout);
      }
      if (annoyingInterval !== null) {
        clearInterval(annoyingInterval);
      }
      grabAttentionTimeout = null;
      annoyingInterval = null;
      if (isPlaying) {
        toggleAnnoying(); // Ensure effect is reset
        isPlaying = false;
      }
    }

    // Function to toggle the annoying effect (sound and screen color)
    function toggleAnnoying() {
      if (!isPlaying) {
        // Start playing tone
        oscillator = audioContext.createOscillator();
        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(2000, audioContext.currentTime);
        oscillator.connect(audioContext.destination);
        oscillator.start();

        // Change screen color to red
        document.body.style.backgroundColor = 'red';
      } else {
        // Stop playing tone and reset screen color
        oscillator?.stop();
        oscillator = null;
        document.body.style.backgroundColor = '';
      }
      isPlaying = !isPlaying;
    }

    // Connect to notebook action to initiate grabAttention after cell execution
    NotebookActions.selectionExecuted.connect(() => {
      if (extensionEnabled) {
        if (grabAttentionTimeout !== null) {
          clearTimeout(grabAttentionTimeout);
        }
        grabAttentionTimeout = setTimeout(grabAttention, 3000) as unknown as number; // Start effect 3 seconds after execution
      }
    });

    // Command to toggle the extension's active state
    app.commands.addCommand('toggle-attention-grabber', {
      label: 'Toggle Attention Grabber',
      execute: () => {
        extensionEnabled = !extensionEnabled;
        if (!extensionEnabled) stopAnnoying();
      }
    });

    // Add context menu item for toggling the extension
    app.contextMenu.addItem({
      command: 'toggle-attention-grabber',
      selector: '.jp-Notebook'
    });

    // Attach event listeners to stop the annoying effect on user interaction
    notebookTracker.widgetAdded.connect((tracker, notebookPanel) => {
      notebookPanel.node.addEventListener('click', stopAnnoying);
      notebookPanel.node.addEventListener('keydown', stopAnnoying);
    });
  }
};

export default plugin;
