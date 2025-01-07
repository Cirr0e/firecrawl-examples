import FirecrawlApp from '@mendable/firecrawl-js'

interface WebSource {
  url: string
  title?: string
  relevanceScore?: number
}

export class ResearchEngine {
  private firecrawl: FirecrawlApp

  constructor(firecrawlApp: FirecrawlApp) {
    this.firecrawl = firecrawlApp
  }

  async findRelevantSources(topic: string, depth: number = 3): Promise<WebSource[]> {
    const searchQuery = `site:*.org OR site:*.edu "${topic}" research`
    
    try {
      // Using Firecrawl's search capabilities
      const searchResult = await this.firecrawl.search({
        query: searchQuery,
        num_results: depth * 5,  // More results to filter
        max_results: depth * 5
      })

      // Basic relevance filtering
      return searchResult.results
        .filter(result => 
          result.url.includes('https://') && 
          !result.url.includes('twitter.com') && 
          !result.url.includes('facebook.com')
        )
        .slice(0, depth)
    } catch (error) {
      console.error('Source search failed:', error)
      return []
    }
  }

  async scrapeSourceContent(sources: WebSource[]): Promise<Array<{url: string, content: string}>> {
    const scrapedContents = []

    for (const source of sources) {
      try {
        const scrapeResult = await this.firecrawl.scrapeUrl(source.url, {
          pageOptions: {
            onlyMainContent: true,
            includeHtml: false
          }
        })

        scrapedContents.push({
          url: source.url,
          content: scrapeResult.data.content || ''
        })
      } catch (error) {
        console.error(`Failed to scrape ${source.url}:`, error)
      }
    }

    return scrapedContents
  }
}