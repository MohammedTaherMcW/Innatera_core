
/**
 * @file
 *
 * @brief Hello World T1 application
 *
 * This application only sends text to the console to demonstrate
 * the build and boot flow for the T1 processor.
 *
 * @copyright (C) Copyright 2024 Innatera Nanosystems B.V.
 **/
#include "utils/console_io.h"
#include "drivers/inn_hal.h"
#include "drivers/inn_cpr.h"

#define TYPER_SPEED_MS  30
#define CURSOR_DELAY_MS 300

static void typer(const char *str)
{
    while (*str) {
        print_char(*str++);
        hal_delay_ms(TYPER_SPEED_MS);
    }
}

static void blinking_cursor(unsigned int reps)
{
    for (int n = 0; n < reps; n++) {
        print_char('_');
        hal_delay_ms(CURSOR_DELAY_MS);
        print_char('\b');
        print_char(' ');
        print_char('\b');
        hal_delay_ms(CURSOR_DELAY_MS);
    }
}

int main(void)
{
    typer("___\n");
    typer("\nWelcome Innaterian!");
    blinking_cursor(1);
    typer("\n");
    blinking_cursor(3);
    typer("\nThis is a demonstration of the build and boot flow for the");
    typer("\nInnatera's Spiking Neural Processor T1, the ultra-low power");
    typer("\nneuromorphic microcontroller for always-on sensing applications.");
    blinking_cursor(2);
    typer("\n");
    typer("\nThe processor uses an ultra-low-power spiking neural network");
    typer("\nengine and a nimble RISC-V processor core to form a single-chip");
    typer("\nsolution for processing sensor data quickly and efficiently.");
    blinking_cursor(2);
    typer("\n");
    typer("\nThe development kit contains more applications that demonstrate");
    typer("\nthe capabilities of the Neural Network accelerators available in T1.");
    blinking_cursor(1);
    typer("\n");
    typer("\nHave fun spiking!");
    blinking_cursor(2);
    typer("\n\n");

    print_string(" _|_|_|  _|      _|  _|      _|    _|_|    _|_|_|_|_|  _|_|_|_|  _|_|_|      _|_|   \n");
    print_string("   _|    _|_|    _|  _|_|    _|  _|    _|      _|      _|        _|    _|  _|    _| \n");
    print_string("   _|    _|  _|  _|  _|  _|  _|  _|_|_|_|      _|      _|_|_|    _|_|_|    _|_|_|_| \n");
    print_string("   _|    _|    _|_|  _|    _|_|  _|    _|      _|      _|        _|    _|  _|    _| \n");
    print_string(" _|_|_|  _|      _|  _|      _|  _|    _|      _|      _|_|_|_|  _|    _|  _|    _| \n");

    return 0;
}
