#!/usr/bin/env node
import { program } from 'commander'
import inquirer from 'inquirer'
import AIResearchAssistant from './index'
import chalk from 'chalk'

async function main() {
  program
    .name('ai-research-assistant')
    .description('CLI for AI-powered web research')
    .version('1.0.0')

  program
    .command('research')
    .description('Conduct research on a specific topic')
    .option('-t, --topic <topic>', 'Research topic')
    .option('-d, --depth <depth>', 'Research depth (number of sources)', '3')
    .action(async (options) => {
      let topic = options.topic

      if (!topic) {
        const answers = await inquirer.prompt([
          {
            type: 'input',
            name: 'topic',
            message: 'Enter the research topic:',
            validate: input => input.length > 0
          }
        ])
        topic = answers.topic
      }

      const depth = parseInt(options.depth, 10)
      
      console.log(chalk.blue(`🔬 Researching: ${topic}`))
      
      const assistant = new AIResearchAssistant()
      
      try {
        const report = await assistant.conductResearch(topic, depth)
        console.log(chalk.green('✅ Research complete. Report generated.'))
      } catch (error) {
        console.error(chalk.red('Research failed:'), error)
      }
    })

  program.parse(process.argv)
}

main()