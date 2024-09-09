import { BarChart } from "@mantine/charts";
import { Card , Center, Text} from "@mantine/core";

type BarChartCardProps = {
    data: any[] | null;
    title: string;
    loading: boolean;
}


export function BarChartCard({ data, title, loading}: BarChartCardProps) {
    if (loading || data == null) {
        return (
            <Card h={300} withBorder>
            </Card>
        )
    } else {
        return (
            <Card withBorder>
                <Center>
                    <Text fw={500}>
                        {title}
                    </Text>
                </Center>
                <br></br>
                <BarChart
                    h={300}
                    dataKey="medium"
                    data={data}
                    type="stacked"
                    orientation="vertical"
                    yAxisProps={{width: 80}}
                    series={[
                        { name: "Available",  color: 'teal.6' },
                        { name: "Unavailable", color: 'red.4' },
                    ]}
                />
            </Card>
        )
    }
}