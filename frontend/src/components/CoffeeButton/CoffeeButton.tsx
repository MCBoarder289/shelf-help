import { Button, Overlay, Transition } from "@mantine/core";
import classes from "./CoffeeButton.module.css"
import { useState } from "react";

export function CoffeeButton() {

    const [isOpen, setIsOpen] = useState(false);

    // Function to toggle the iframe visibility
    const toggleWidget = () => {
        setIsOpen(!isOpen);
    };

    return (
        <div>

            <Button
                className={classes.coffeeButton}
                leftSection={'☕'}
                radius={"md"}
                color="#FFDD00"
                onClick={toggleWidget}
            // component="a"
            // href="https://buymeacoffee.com/michaelchapman"
            // target="_blank"
            >
                Buy me a coffee
            </Button>
            {/* Conditional rendering of the iframe based on state */}
            {isOpen && (
                <Transition
                mounted={isOpen}
                transition='pop'
                duration={200}
                >
                     {(transitionStyles) =>
                    <Overlay  style={transitionStyles} backgroundOpacity={0.55} blur={3} center>
                        <div
                            style={{
                                position: 'relative',
                                width: '100%',
                                height: '100%',
                                maxWidth: '400px', // Max width for desktop
                                maxHeight: '90vh', // 90% of the viewport height for desktop
                                backgroundColor: 'white',
                                borderRadius: '10px',
                                overflow: 'hidden',
                                display: 'flex',
                                justifyContent: 'center',
                                ...transitionStyles
                            }}
                        >
                            <iframe
                                src="https://www.buymeacoffee.com/widget/page/michaelchapman?description=support-me&color=%23FFDD00"
                                title="Buy Me a Coffee"
                                style={{
                                    width: '100%',
                                    height: '100%',
                                    border: 'none',
                                }}
                                allow="payment"
                            ></iframe>

                            {/* Close button */}
                            <button
                                onClick={toggleWidget}
                                style={{
                                    position: 'absolute',
                                    top: '10px',
                                    right: '10px',
                                    background: 'red',
                                    color: 'white',
                                    border: 'none',
                                    borderRadius: '50%',
                                    width: '30px',
                                    height: '30px',
                                    cursor: 'pointer',
                                }}
                            >
                                X
                            </button>
                        </div>
                    </Overlay>
                    }
                </Transition>
            )}
        </div>
    )
}