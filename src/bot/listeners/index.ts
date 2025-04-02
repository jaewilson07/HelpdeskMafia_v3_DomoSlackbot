import { register as registerCommands } from './commands';
import { register as registerEvents } from './events';

export function registerListeners() {
    // Register commands
    registerCommands();

    // Register events
    registerEvents();

    console.log('All listeners registered');
}
