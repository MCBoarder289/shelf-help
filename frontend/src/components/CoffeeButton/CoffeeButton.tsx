import { Button, Modal, CloseButton} from "@mantine/core";
import classes from "./CoffeeButton.module.css"
import { useDisclosure } from "@mantine/hooks";

export function CoffeeButton() {

    const [opened, { open, close }] = useDisclosure(false);

    return (
        <>
        <Button
            className={classes.coffeeButton}
            leftSection={'☕'}
            radius={"md"}
            color="#FFDD00"
            onClick={open}
        >
            Buy me a coffee
        </Button>
        <Modal
                opened={opened}
                onClose={close}
                withCloseButton={false} // Disable default close button
                size="400px"
                overlayProps={{
                    backgroundOpacity: 0.55,
                    blur: 3,
                }}
                styles={{
                    body: {
                        padding: 0, // Remove default padding
                        maxWidth: "400px",
                        width: "100%",
                        height: "90vh",
                        borderRadius: "10px",
                        display: "flex",
                        justifyContent: "center",
                        overflow: "hidden", // Prevent scrollbars
                    },
                }}
            >
                <div
                    style={{
                        position: "relative",
                        width: "100%",
                        height: "100%",
                        backgroundColor: "white",
                        borderRadius: "10px",
                        overflow: "hidden",
                        display: "flex",
                        justifyContent: "center",
                    }}
                >
                    <iframe
                        src="https://www.buymeacoffee.com/widget/page/michaelchapman?description=support-me&color=%23FFDD00"
                        title="Buy Me a Coffee"
                        style={{
                            width: "100%",
                            height: "100%",
                            border: "none",
                            overflow: "hidden", // Prevent iframe scroll
                        }}
                        allow="payment"
                    ></iframe>

                    {/* Mantine Close Button */}
                    <CloseButton
                        onClick={close}
                        style={{
                            position: "absolute",
                            top: "10px",
                            right: "10px",
                           
                        }}
                    />
                </div>
            </Modal>
        </>
    )
}