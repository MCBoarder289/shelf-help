import { Button } from "@mantine/core";
import { IconBrandGithub } from "@tabler/icons-react";

export function GithubButton() {

    const icon = <IconBrandGithub size={15} />;

    return (
       <Button
        leftSection={icon}
        radius={"md"}
        component="a"
        href="https://github.com/MCBoarder289/shelf-help"
        target="_blank"
        color="#be4bdb"//{"var(--mantine-color-grape-6)}"
       >
        Source
       </Button>
    )
}