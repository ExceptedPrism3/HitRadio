const fs = require('fs');
const path = require('path');

const logsDir = path.join(__dirname, '..', 'logs');

if (!fs.existsSync(logsDir)) {
  fs.mkdirSync(logsDir);
}

function getFormattedDate() {
  const date = new Date();
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const year = date.getFullYear();
  return `${day}-${month}-${year}`;
}

let currentLogDate = getFormattedDate();
let logStream = fs.createWriteStream(path.join(logsDir, `${currentLogDate}.log`), { flags: 'a' });

function ensureLogFile() {
  const today = getFormattedDate();
  if (today !== currentLogDate) {
    // Date changed, close old stream and create new one
    logStream.end();
    currentLogDate = today;
    logStream = fs.createWriteStream(path.join(logsDir, `${currentLogDate}.log`), { flags: 'a' });
  }
}

const originalConsoleLog = console.log;
const originalConsoleError = console.error;
const originalConsoleWarn = console.warn;
const originalConsoleInfo = console.info;

function logToFile(message) {
    ensureLogFile();
    const timestamp = new Date().toISOString();
    logStream.write(`[${timestamp}] ${message}\n`);
}

console.log = (...args) => {
  const message = args.join(' ');
  logToFile(`LOG: ${message}`);
  originalConsoleLog.apply(console, args);
};

console.error = (...args) => {
  const message = args.join(' ');
  logToFile(`ERROR: ${message}`);
  originalConsoleError.apply(console, args);
};

console.warn = (...args) => {
    const message = args.join(' ');
    logToFile(`WARN: ${message}`);
    originalConsoleWarn.apply(console, args);
};

console.info = (...args) => {
    const message = args.join(' ');
    logToFile(`INFO: ${message}`);
    originalConsoleInfo.apply(console, args);
};

module.exports = {
  log: console.log,
  error: console.error,
  warn: console.warn,
  info: console.info,
};
