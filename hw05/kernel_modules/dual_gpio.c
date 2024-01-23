#include <linux/gpio.h>
#include <linux/init.h>
#include <linux/interrupt.h>
#include <linux/kernel.h>
#include <linux/module.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Jailen Hobbs");
MODULE_DESCRIPTION("A Button/LED test driver for the BeagleBone");
MODULE_VERSION("0.2");

static unsigned int gpioLED1 = 60;     // P9_12 (GPIO60)
static unsigned int gpioLED2 = 50;     // P9_14 (GPIO50)
static unsigned int gpioButton1 = 47;  // P8_15 (GPIO47)
static unsigned int gpioButton2 = 65;  // P8_18 (GPIO65)
static unsigned int irqNumber1, irqNumber2;
static bool ledOn1 = 0;  // Is LED1 on or off
static bool ledOn2 = 0;  // Is LED2 on or off

// prototype for the custom IRQ handler function
static irq_handler_t ebb_gpio_irq_handler(unsigned int irq, void *dev_id, struct pt_regs *regs);

static int __init ebb_gpio_init(void) {
  int result = 0;
  printk(KERN_INFO "GPIO_TEST: Initializing the GPIO_TEST LKM\n");

  // LED1 setup
  gpio_request(gpioLED1, "sysfs");
  gpio_direction_output(gpioLED1, ledOn1);
  gpio_export(gpioLED1, false);

  // Button1 setup
  gpio_request(gpioButton1, "sysfs");
  gpio_direction_input(gpioButton1);
  gpio_export(gpioButton1, false);
  irqNumber1 = gpio_to_irq(gpioButton1);
  result = request_irq(irqNumber1, (irq_handler_t)ebb_gpio_irq_handler, IRQF_TRIGGER_RISING, "ebb_gpio_handler1", NULL);

  // LED2 setup
  gpio_request(gpioLED2, "sysfs");
  gpio_direction_output(gpioLED2, ledOn2);
  gpio_export(gpioLED2, false);

  // Button2 setup
  gpio_request(gpioButton2, "sysfs");
  gpio_direction_input(gpioButton2);
  gpio_export(gpioButton2, false);
  irqNumber2 = gpio_to_irq(gpioButton2);
  result = request_irq(irqNumber2, (irq_handler_t)ebb_gpio_irq_handler, IRQF_TRIGGER_RISING, "ebb_gpio_handler2", NULL);

  return result;
}

static void __exit ebb_gpio_exit(void) {
  // Turn off LEDs and cleanup
  gpio_set_value(gpioLED1, 0);
  gpio_unexport(gpioLED1);
  free_irq(irqNumber1, NULL);
  gpio_unexport(gpioButton1);
  gpio_free(gpioLED1);
  gpio_free(gpioButton1);

  gpio_set_value(gpioLED2, 0);
  gpio_unexport(gpioLED2);
  free_irq(irqNumber2, NULL);
  gpio_unexport(gpioButton2);
  gpio_free(gpioLED2);
  gpio_free(gpioButton2);

  printk(KERN_INFO "GPIO_TEST: Goodbye from the LKM!\n");
}

static irq_handler_t ebb_gpio_irq_handler(unsigned int irq, void *dev_id, struct pt_regs *regs) {
  if (irq == irqNumber1) {
    ledOn1 = !ledOn1;
    gpio_set_value(gpioLED1, ledOn1);
  } else if (irq == irqNumber2) {
    ledOn2 = !ledOn2;
    gpio_set_value(gpioLED2, ledOn2);
  }
  return (irq_handler_t)IRQ_HANDLED;
}

module_init(ebb_gpio_init);
module_exit(ebb_gpio_exit);
