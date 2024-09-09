import { AreaChart } from "@mantine/charts";
import { Card , Center, Text} from "@mantine/core";

type AreaChartCardProps = {
    data: any[] | null;
    title: string;
    loading: boolean;
    yAxisLimit: number;
}


export function AreaChartCard({ data, title, loading, yAxisLimit}: AreaChartCardProps) {
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
                <AreaChart
                    h={300}
                    dataKey='date_axis'
                    data={data}
                    curveType='monotone'
                    withDots={false}
                    yAxisProps={{ domain: [0, yAxisLimit] }}
                    xAxisProps={{ angle: -20 }}
                    series={[
                        { name: 'Cumulative Shelf Count', color: 'indigo.6' }
                    ]}
                    areaProps={{ isAnimationActive: true, animationDuration: 3000, animationEasing: 'ease' }}
                />
            </Card>
        )
    }
}