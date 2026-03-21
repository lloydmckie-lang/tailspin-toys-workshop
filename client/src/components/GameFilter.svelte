<script lang="ts">
    // GameFilter component — provides category and publisher dropdowns for filtering games.
    interface FilterOption {
        id: number;
        name: string;
    }

    let {
        selectedCategory = $bindable(''),
        selectedPublisher = $bindable(''),
    }: {
        selectedCategory?: string;
        selectedPublisher?: string;
    } = $props();

    let categories = $state<FilterOption[]>([]);
    let publishers = $state<FilterOption[]>([]);

    const hasActiveFilters = $derived(selectedCategory !== '' || selectedPublisher !== '');

    $effect(() => {
        Promise.all([
            fetch('/api/categories').then(r => r.json()),
            fetch('/api/publishers').then(r => r.json()),
        ]).then(([cats, pubs]) => {
            categories = cats;
            publishers = pubs;
        });
    });

    function clearFilters(): void {
        selectedCategory = '';
        selectedPublisher = '';
    }
</script>

<div class="flex flex-wrap items-end gap-4 mb-6 p-4 bg-slate-800/60 rounded-xl border border-slate-700/50" data-testid="game-filter">
    <div class="flex flex-col gap-1">
        <label for="category-filter" class="text-sm font-medium text-slate-300">Category</label>
        <select
            id="category-filter"
            bind:value={selectedCategory}
            class="bg-slate-700 text-slate-100 border border-slate-600 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 hover:border-slate-500 transition-colors"
            data-testid="category-filter"
        >
            <option value="">All Categories</option>
            {#each categories as category (category.id)}
                <option value={category.name}>{category.name}</option>
            {/each}
        </select>
    </div>

    <div class="flex flex-col gap-1">
        <label for="publisher-filter" class="text-sm font-medium text-slate-300">Publisher</label>
        <select
            id="publisher-filter"
            bind:value={selectedPublisher}
            class="bg-slate-700 text-slate-100 border border-slate-600 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 hover:border-slate-500 transition-colors"
            data-testid="publisher-filter"
        >
            <option value="">All Publishers</option>
            {#each publishers as publisher (publisher.id)}
                <option value={publisher.name}>{publisher.name}</option>
            {/each}
        </select>
    </div>

    {#if hasActiveFilters}
        <button
            onclick={clearFilters}
            class="px-4 py-2 text-sm font-medium text-slate-300 bg-slate-700 border border-slate-600 rounded-lg hover:bg-slate-600 hover:text-slate-100 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
            data-testid="clear-filters-button"
        >
            Clear Filters
        </button>
    {/if}
</div>
