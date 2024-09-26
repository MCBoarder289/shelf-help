import { PieChart } from "@mantine/charts";
import { Card , Center, Text} from "@mantine/core";

type BarChartCardProps = {
    data: any[] | null;
    title: string;
    loading: boolean;
}


export function SearchTypePieChartCard({ data, title, loading}: BarChartCardProps) {
    if (loading || data == null) {
        return (
            <Card h={300} withBorder>
            </Card>
        )
    } else {
        console.log(data)
        return (
            <Card withBorder>
                <Center>
                    <Text fw={500}>
                        {title}
                    </Text>
                </Center>
                <br></br>
                <Center>
                <PieChart
                    h={300}
                    data={data}
                    withLabelsLine={false} 
                    labelsPosition="outside" 
                    labelsType="percent" 
                    size={250}
                    withLabels
                    withTooltip
                />
                </Center>
            </Card>
        )
    }
}