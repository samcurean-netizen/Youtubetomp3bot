/**
 * Pipedream Component for Telegram Bot Webhook
 * 
 * This is a Node.js component that calls Python code for processing.
 * Alternatively, you can use the Python code directly in a Python step.
 */

export default {
  name: "Telegram Bot Webhook Handler",
  version: "0.0.1",
  key: "telegram-bot-webhook",
  description: "Processes Telegram bot webhooks for YouTube downloads and audio transcription",
  type: "action",
  props: {
    // HTTP trigger is automatic when used as a webhook
  },
  async run({ steps, $ }) {
    // The webhook payload from Telegram is in steps.trigger.event.body
    const update = steps.trigger.event.body;
    
    if (!update) {
      return {
        statusCode: 400,
        body: "No update received"
      };
    }

    // Log the update for debugging
    console.log("Received update:", JSON.stringify(update, null, 2));

    // Return success - actual processing should be done in a Python step
    return {
      statusCode: 200,
      body: "OK"
    };
  },
};
