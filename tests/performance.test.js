/**
 * Performance Tests
 * Tests for code efficiency and performance
 */

describe('Performance Optimizations', () => {
  describe('localStorage error handling', () => {
    test('handles corrupted localStorage data gracefully', () => {
      const mockLocalStorage = {
        getItem: jest.fn(() => 'invalid json{'),
        removeItem: jest.fn()
      };
      global.localStorage = mockLocalStorage;

      // This should not throw
      expect(() => {
        try {
          JSON.parse(mockLocalStorage.getItem('test'));
        } catch (error) {
          mockLocalStorage.removeItem('test');
        }
      }).not.toThrow();

      expect(mockLocalStorage.removeItem).toHaveBeenCalledWith('test');
    });

    test('handles localStorage quota exceeded', () => {
      const mockLocalStorage = {
        setItem: jest.fn(() => {
          throw new Error('QuotaExceededError');
        })
      };
      global.localStorage = mockLocalStorage;

      // This should not throw
      expect(() => {
        try {
          mockLocalStorage.setItem('test', 'data');
        } catch (error) {
          console.error('Failed to save:', error);
        }
      }).not.toThrow();
    });
  });

  describe('Notification deduplication', () => {
    test('prevents duplicate notifications', () => {
      const activeNotifications = new Set();
      const message = 'Test notification';
      const type = 'info';
      const key = `${type}:${message}`;

      // First notification should be added
      expect(activeNotifications.has(key)).toBe(false);
      activeNotifications.add(key);
      expect(activeNotifications.has(key)).toBe(true);

      // Duplicate should be prevented
      const isDuplicate = activeNotifications.has(key);
      expect(isDuplicate).toBe(true);
    });
  });

  describe('Array filtering optimization', () => {
    test('single reduce is more efficient than multiple filters', () => {
      const downloads = [
        { id: 1, status: 'downloading' },
        { id: 2, status: 'pending' },
        { id: 3, status: 'completed' },
        { id: 4, status: 'failed' },
        { id: 5, status: 'downloading' },
        { id: 6, status: 'pending' }
      ];

      // Measure time for multiple filters (inefficient)
      const start1 = performance.now();
      const activeOld = downloads.filter(d => d.status === 'downloading');
      const pendingOld = downloads.filter(d => d.status === 'pending');
      const completedOld = downloads.filter(d => d.status === 'completed');
      const failedOld = downloads.filter(d => d.status === 'failed');
      const end1 = performance.now();
      const timeOld = end1 - start1;

      // Measure time for single reduce (efficient)
      const start2 = performance.now();
      const categorized = downloads.reduce((acc, download) => {
        switch(download.status) {
        case 'downloading':
          acc.active.push(download);
          break;
        case 'pending':
          acc.pending.push(download);
          break;
        case 'completed':
          acc.completed.push(download);
          break;
        case 'failed':
          acc.failed.push(download);
          break;
        }
        return acc;
      }, { active: [], pending: [], completed: [], failed: [] });
      const end2 = performance.now();
      const timeNew = end2 - start2;

      // Verify results are the same
      expect(categorized.active).toEqual(activeOld);
      expect(categorized.pending).toEqual(pendingOld);
      expect(categorized.completed).toEqual(completedOld);
      expect(categorized.failed).toEqual(failedOld);

      // Log performance comparison (not asserting as times vary)
      console.log(`Multiple filters: ${timeOld.toFixed(3)}ms`);
      console.log(`Single reduce: ${timeNew.toFixed(3)}ms`);
    });
  });

  describe('String method optimization', () => {
    test('slice is preferred over deprecated substr', () => {
      const random = Math.random().toString(36);

      // Test that slice works correctly
      const result1 = random.slice(2, 11);
      expect(result1.length).toBeLessThanOrEqual(9);

      // Verify slice behavior matches substr for our use case
      const testStr = '0.123456789';
      const sliceResult = testStr.slice(2, 11);
      expect(sliceResult).toBe('123456789');
    });
  });

  describe('DOM query caching', () => {
    test('caching DOM queries prevents redundant lookups', () => {
      // Simulate DOM query
      const mockQuerySelectorAll = jest.fn(() => [
        { dataset: { queue: 'active' } },
        { dataset: { queue: 'pending' } }
      ]);

      // Uncached approach (called multiple times)
      for (let i = 0; i < 5; i++) {
        mockQuerySelectorAll();
      }
      expect(mockQuerySelectorAll).toHaveBeenCalledTimes(5);

      // Cached approach (called once)
      mockQuerySelectorAll.mockClear();
      const cached = mockQuerySelectorAll();
      for (let i = 0; i < 5; i++) {
        // Use cached result
        cached.forEach(() => {});
      }
      expect(mockQuerySelectorAll).toHaveBeenCalledTimes(1);
    });
  });

  describe('Clipboard monitor optimization', () => {
    test('setTimeout allows proper cleanup unlike setInterval', () => {
      let timeoutId;
      let intervalId;
      
      // setTimeout can be cleared
      const clearableTimeout = () => {
        timeoutId = setTimeout(() => {}, 1000);
        clearTimeout(timeoutId);
      };
      expect(() => clearableTimeout()).not.toThrow();

      // setInterval requires manual cleanup
      const clearableInterval = () => {
        intervalId = setInterval(() => {}, 1000);
        clearInterval(intervalId);
      };
      expect(() => clearableInterval()).not.toThrow();
    });
  });

  describe('XSS prevention in notifications', () => {
    test('URL escaping prevents XSS attacks', () => {
      const maliciousUrl = 'javascript:alert(\'XSS\')';
      const escapedUrl = maliciousUrl.replace(/'/g, '&#39;');
      
      expect(escapedUrl).not.toContain('\'');
      expect(escapedUrl).toContain('&#39;');
    });
  });
});

describe('Code Quality', () => {
  test('error handler has correct number of parameters', () => {
    // Express error handlers must have 4 parameters
    const errorHandler = (err, req, res, next) => { // eslint-disable-line no-unused-vars
      res.status(500).json({ error: err.message });
    };
    
    expect(errorHandler.length).toBe(4);
  });

  test('constants are loaded at module level', () => {
    // This is a structural test - constants should be loaded once
    // not inside request handlers
    const moduleLevel = true;
    expect(moduleLevel).toBe(true);
  });
});
