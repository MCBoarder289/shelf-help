import { Card, Center, NumberFormatter, Stack, Text } from "@mantine/core";
import classes from './NumberIndicator.module.css';


type NumberIndicatorProps = {
    title: string;
    value: number | null;
    suffix?: string | null;
}

export function NumberIndicator({title, value, suffix = null}: NumberIndicatorProps) {
    return (
        <Card withBorder>
            <Center>
                <Stack align="stretch" justify="center">
                    <Text fw={500}>
                        {title}
                    </Text>
                    <Center>
                        <NumberFormatter thousandSeparator value={value ? value : undefined} className={classes.number}  suffix={suffix ? suffix : undefined}/>
                    </Center>
                </Stack>
            </Center>
        </Card>
    )
}