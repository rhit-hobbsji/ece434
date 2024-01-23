#include <linux/delay.h>
#include <linux/gpio.h>
#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/kobject.h>
#include <linux/kthread.h>
#include <linux/module.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Derek Molloy");
MODULE_DESCRIPTION("A simple Linux LED driver LKM for the BBB");
MODULE_VERSION("0.1");

static unsigned int gpioLED1 = 49;        // GPIO for the first LED
static unsigned int gpioLED2 = 15;        // GPIO for the second LED
static unsigned int blinkPeriod1 = 1000;  // The blink period in ms for the first LED
static unsigned int blinkPeriod2 = 500;   // The blink period in ms for the second LED

static struct task_struct *task1;  // The pointer to the first thread task
static struct task_struct *task2;  // The pointer to the second thread task

// Function prototype for the LED flashing thread
static int flash(void *arg);

static int flash(void *arg) {
  unsigned int gpioLED = *(unsigned int *)arg;
  bool ledOn = 0;
  unsigned int blinkPeriod = (gpioLED == gpioLED1) ? blinkPeriod1 : blinkPeriod2;

  printk(KERN_INFO "EBB LED: Thread has started running for GPIO %d\n", gpioLED);
  while (!kthread_should_stop()) {
    set_current_state(TASK_RUNNING);
    ledOn = !ledOn;
    gpio_set_value(gpioLED, ledOn);
    set_current_state(TASK_INTERRUPTIBLE);
    msleep(blinkPeriod / 2);
  }
  printk(KERN_INFO "EBB LED: Thread has run to completion for GPIO %d\n", gpioLED);
  return 0;
}

static int __init ebbLED_init(void) {
  printk(KERN_INFO "EBB LED: Initializing the EBB LED LKM\n");

  gpio_request(gpioLED1, "sysfs");
  gpio_direction_output(gpioLED1, false);
  gpio_export(gpioLED1, false);

  gpio_request(gpioLED2, "sysfs");
  gpio_direction_output(gpioLED2, false);
  gpio_export(gpioLED2, false);

  task1 = kthread_run(flash, &gpioLED1, "LED1_flash_thread");
  if (IS_ERR(task1)) {
    printk(KERN_ALERT "EBB LED: Failed to create the task for LED1\n");
    gpio_free(gpioLED1);
    return PTR_ERR(task1);
  }

  task2 = kthread_run(flash, &gpioLED2, "LED2_flash_thread");
  if (IS_ERR(task2)) {
    printk(KERN_ALERT "EBB LED: Failed to create the task for LED2\n");
    kthread_stop(task1);
    gpio_free(gpioLED1);
    gpio_free(gpioLED2);
    return PTR_ERR(task2);
  }
  return 0;
}

static void __exit ebbLED_exit(void) {
  kthread_stop(task1);
  kthread_stop(task2);

  gpio_set_value(gpioLED1, 0);
  gpio_unexport(gpioLED1);
  gpio_free(gpioLED1);

  gpio_set_value(gpioLED2, 0);
  gpio_unexport(gpioLED2);
  gpio_free(gpioLED2);

  printk(KERN_INFO "EBB LED: Goodbye from the EBB LED LKM!\n");
}

module_init(ebbLED_init);
module_exit(ebbLED_exit);
