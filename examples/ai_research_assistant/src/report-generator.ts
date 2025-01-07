import OpenAI from 'openai'
import fs from 'fs/promises'
import path from 'path'

interface ReportData {
  topic: string
  sources: Array<{url: string, title?: string}>
  content: Array<{url: string, content: string}>
  insights: string
}

export class ReportGenerator {
  private openai: OpenAI

  constructor(openaiClient: OpenAI) {
    this.openai = openaiClient
  }

  async generateInsights(
    scrapedContent: Array<{url: string, content: string}>, 
    topic: string
  ): Promise<string> {
    const combinedContent = scrapedContent
      .map(source => source.content)
      .join('\n\n')

    try {
      const completion = await this.openai.chat.completions.create({
        model: 'gpt-4-1106-preview',
        messages: [
          {
            role: 'system', 
            content: 'You are an expert research analyst synthesizing key insights from web research.'
          },
          {
            role: 'user',
            content: `Analyze the following research content about ${topic}. 
            Provide a concise, structured summary highlighting:
            1. Key trends
            2. Emerging insights
            3. Potential implications
            4. Critical perspectives

            Research Content:\n${combinedContent.slice(0, 15000)}`
          }
        ],
        max_tokens: 1500,
        temperature: 0.7
      })

      return completion.choices[0].message.content || 'No insights generated'
    } catch (error) {
      console.error('Insight generation failed:', error)
      return 'Insight generation encountered an error'
    }
  }

  async createReport(reportData: ReportData): Promise<string> {
    const reportContent = `
# Research Report: ${reportData.topic}

## Sources
${reportData.sources.map(source => `- ${source.title || source.url}`).join('\n')}

## Key Insights
${reportData.insights}

## Detailed Research Notes
${reportData.content.map(source => 
  `### Source: ${source.url}\n${source.content.slice(0, 500)}...`
).join('\n\n')}
    `

    // Save report to file
    const reportDir = path.join(process.cwd(), 'reports')
    await fs.mkdir(reportDir, { recursive: true })
    
    const filename = `research_${Date.now()}.md`
    const fullPath = path.join(reportDir, filename)
    
    await fs.writeFile(fullPath, reportContent)
    
    return reportContent
  }
}