import { BarChart } from "@mantine/charts";
import { Card , Center, Text} from "@mantine/core";

type HourlyBarChartCardProps = {
    data: any[] | null;
    title: string;
    loading: boolean;
}


export function HourlyBarChartCard({ data, title, loading}: HourlyBarChartCardProps) {
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
                    dataKey="Hour"
                    data={data}
                    barProps={{ radius: 5 }}
                    yAxisProps={{width: 80}}
                    series={[
                        { name: "Searches",  color: 'indigo.6' },
                    ]}
                />
            </Card>
        )
    }
}