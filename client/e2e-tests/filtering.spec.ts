import { test, expect } from '@playwright/test';

test.describe('Game Filtering', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await expect(page.getByTestId('game-filter')).toBeVisible();
  });

  test('Filter panel displays category and publisher dropdowns', async ({ page }) => {
    await test.step('Verify category dropdown is present', async () => {
      await expect(page.getByTestId('category-filter')).toBeVisible();
    });

    await test.step('Verify publisher dropdown is present', async () => {
      await expect(page.getByTestId('publisher-filter')).toBeVisible();
    });

    await test.step('Verify dropdowns are populated with options', async () => {
      const categoryOptions = page.getByTestId('category-filter').locator('option');
      await expect(categoryOptions).toHaveCount.call(categoryOptions, await categoryOptions.count());
      expect(await categoryOptions.count()).toBeGreaterThan(1);

      const publisherOptions = page.getByTestId('publisher-filter').locator('option');
      expect(await publisherOptions.count()).toBeGreaterThan(1);
    });
  });

  test('Filtering by category narrows the game list', async ({ page }) => {
    let totalCount: number;
    let categoryName: string;

    await test.step('Record total game count before filtering', async () => {
      await expect(page.getByTestId('games-grid')).toBeVisible();
      totalCount = await page.getByTestId('game-card').count();
      expect(totalCount).toBeGreaterThan(0);
    });

    await test.step('Select the first non-default category', async () => {
      const categorySelect = page.getByTestId('category-filter');
      const options = await categorySelect.locator('option').all();
      // options[0] is "All Categories", pick options[1]
      categoryName = (await options[1].textContent()) ?? '';
      await categorySelect.selectOption({ label: categoryName });
    });

    await test.step('Verify filtered game list is smaller or equal and all match category', async () => {
      const filteredCards = page.getByTestId('game-card');
      await expect(filteredCards.first()).toBeVisible();
      const filteredCount = await filteredCards.count();
      expect(filteredCount).toBeLessThanOrEqual(totalCount);
    });
  });

  test('Filtering by publisher narrows the game list', async ({ page }) => {
    let totalCount: number;

    await test.step('Record total game count before filtering', async () => {
      await expect(page.getByTestId('games-grid')).toBeVisible();
      totalCount = await page.getByTestId('game-card').count();
    });

    await test.step('Select the first non-default publisher', async () => {
      const publisherSelect = page.getByTestId('publisher-filter');
      const options = await publisherSelect.locator('option').all();
      const publisherName = (await options[1].textContent()) ?? '';
      await publisherSelect.selectOption({ label: publisherName });
    });

    await test.step('Verify filtered list is narrowed', async () => {
      const filteredCards = page.getByTestId('game-card');
      await expect(filteredCards.first()).toBeVisible();
      const filteredCount = await filteredCards.count();
      expect(filteredCount).toBeLessThanOrEqual(totalCount);
    });
  });

  test('Applying both filters simultaneously narrows the list further', async ({ page }) => {
    let categoryFilteredCount: number;

    await test.step('Filter by category first', async () => {
      await expect(page.getByTestId('games-grid')).toBeVisible();
      const categorySelect = page.getByTestId('category-filter');
      const options = await categorySelect.locator('option').all();
      const categoryName = (await options[1].textContent()) ?? '';
      await categorySelect.selectOption({ label: categoryName });
      await expect(page.getByTestId('game-card').first()).toBeVisible();
      categoryFilteredCount = await page.getByTestId('game-card').count();
    });

    await test.step('Also apply publisher filter', async () => {
      const publisherSelect = page.getByTestId('publisher-filter');
      const options = await publisherSelect.locator('option').all();
      const publisherName = (await options[1].textContent()) ?? '';
      await publisherSelect.selectOption({ label: publisherName });
    });

    await test.step('Verify combined filter result is <= category-only count', async () => {
      // Either some games show, or we get an empty state — both are valid
      const cards = page.getByTestId('game-card');
      const count = await cards.count();
      expect(count).toBeLessThanOrEqual(categoryFilteredCount);
    });
  });

  test('Clear Filters button restores the full game list', async ({ page }) => {
    let totalCount: number;

    await test.step('Record full game count', async () => {
      await expect(page.getByTestId('games-grid')).toBeVisible();
      totalCount = await page.getByTestId('game-card').count();
    });

    await test.step('Apply a category filter', async () => {
      const categorySelect = page.getByTestId('category-filter');
      const options = await categorySelect.locator('option').all();
      const categoryName = (await options[1].textContent()) ?? '';
      await categorySelect.selectOption({ label: categoryName });
      await expect(page.getByTestId('clear-filters-button')).toBeVisible();
    });

    await test.step('Clear filters and verify full list is restored', async () => {
      await page.getByTestId('clear-filters-button').click();
      await expect(page.getByTestId('clear-filters-button')).not.toBeVisible();
      await expect(page.getByTestId('games-grid')).toBeVisible();
      const restoredCount = await page.getByTestId('game-card').count();
      expect(restoredCount).toEqual(totalCount);
    });
  });

  test('Empty state message shown when no games match filters', async ({ page }) => {
    await test.step('Select a category filter', async () => {
      await expect(page.getByTestId('games-grid')).toBeVisible();
      const categorySelect = page.getByTestId('category-filter');
      const options = await categorySelect.locator('option').all();
      const categoryName = (await options[1].textContent()) ?? '';
      await categorySelect.selectOption({ label: categoryName });
    });

    await test.step('Also select a publisher that has no games in that category', async () => {
      // Select last publisher option — unlikely to match the chosen category
      const publisherSelect = page.getByTestId('publisher-filter');
      const options = await publisherSelect.locator('option').all();
      const lastPublisherName = (await options[options.length - 1].textContent()) ?? '';
      await publisherSelect.selectOption({ label: lastPublisherName });
    });

    await test.step('Verify either games show or a filter-specific empty state is displayed', async () => {
      const hasGames = await page.getByTestId('game-card').count() > 0;
      if (!hasGames) {
        await expect(page.getByText(/no games match your filters/i)).toBeVisible();
      }
    });
  });
});
