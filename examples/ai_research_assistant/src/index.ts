import * as dotenv from 'dotenv'
import FirecrawlApp from '@mendable/firecrawl-js'
import OpenAI from 'openai'
import { ResearchEngine } from './research-engine'
import { ReportGenerator } from './report-generator'
import chalk from 'chalk'

dotenv.config()

class AIResearchAssistant {
  private firecrawl: FirecrawlApp
  private openai: OpenAI
  private researchEngine: ResearchEngine
  private reportGenerator: ReportGenerator

  constructor() {
    if (!process.env.FIRECRAWL_API_KEY || !process.env.OPENAI_API_KEY) {
      throw new Error('Missing API keys. Check your .env file.')
    }

    this.firecrawl = new FirecrawlApp({ 
      apiKey: process.env.FIRECRAWL_API_KEY 
    })
    
    this.openai = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY
    })

    this.researchEngine = new ResearchEngine(this.firecrawl)
    this.reportGenerator = new ReportGenerator(this.openai)
  }

  async conductResearch(topic: string, depth: number = 3) {
    console.log(chalk.blue(`🔍 Initiating research on: ${topic}`))

    // Perform web research
    const webSources = await this.researchEngine.findRelevantSources(topic, depth)
    console.log(chalk.green(`✅ Found ${webSources.length} relevant sources`))

    // Scrape and extract content
    const scrapedContent = await this.researchEngine.scrapeSourceContent(webSources)
    console.log(chalk.green(`📄 Extracted content from sources`))

    // Generate AI-powered insights
    const insights = await this.reportGenerator.generateInsights(scrapedContent, topic)
    console.log(chalk.green(`💡 Generated AI insights`))

    // Create comprehensive report
    const report = await this.reportGenerator.createReport({
      topic,
      sources: webSources,
      content: scrapedContent,
      insights
    })

    console.log(chalk.blue(`📊 Research complete. Report generated.`))
    return report
  }
}

// Example usage
async function main() {
  const assistant = new AIResearchAssistant()
  
  try {
    const report = await assistant.conductResearch('AI Ethics in 2024')
    console.log(report)
  } catch (error) {
    console.error(chalk.red('Research failed:'), error)
  }
}

// Uncomment to run directly
// main()

export default AIResearchAssistant