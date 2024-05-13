import { Button } from "@mantine/core";
import classes from "./CoffeeButton.module.css"

export function CoffeeButton() {
    return (
        <Button
        className={classes.coffeeButton}
        leftSection={'☕'}
        radius={"md"}
        color="#FFDD00"
        component="a"
        href="https://buymeacoffee.com/michaelchapman"
        target="_blank"
        >
         Buy me a coffee
        </Button>
    )
}