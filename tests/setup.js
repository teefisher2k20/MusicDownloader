// Jest setup file
// This runs before all tests

// Mock browser APIs
global.localStorage = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn()
};

global.sessionStorage = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn()
};

// Mock Notification API
global.Notification = class {
  constructor(title, options) {
    this.title = title;
    this.options = options;
  }
  static permission = 'granted';
  static requestPermission = jest.fn(() => Promise.resolve('granted'));
};

// Mock Clipboard API
global.navigator.clipboard = {
  readText: jest.fn(() => Promise.resolve('')),
  writeText: jest.fn(() => Promise.resolve())
};

// Console error suppression for expected errors
const originalError = console.error;
beforeAll(() => {
  console.error = (...args) => {
    if (
      typeof args[0] === 'string' &&
      args[0].includes('Not implemented: HTMLFormElement.prototype.submit')
    ) {
      return;
    }
    originalError.call(console, ...args);
  };
});

afterAll(() => {
  console.error = originalError;
});
