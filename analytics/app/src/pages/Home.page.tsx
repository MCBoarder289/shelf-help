import { AppShell, Container, rem, SimpleGrid, Skeleton, SegmentedControl} from '@mantine/core';
import { HeaderSimple } from "../components/HeaderSimple/HeaderSimple";
import { createClient } from '@supabase/supabase-js'
import { Database } from '../../database.types.ts'
import { SetStateAction, useEffect, useState } from 'react';
import { NumberIndicator } from '../components/NumberIndicator/NumberIndicator.tsx';
import { AreaChartCard } from '../components/AreaChartCard/AreaChartCard.tsx';
import { BarChartCard } from '../components/BarChartCard/BarChartCard.tsx';
import { HourlyBarChartCard } from '../components/HourlyBarChartCard/HourlyBarChartCard.tsx';

// Create a single supabase client for interacting with your database
const supabase = createClient<Database>('https://hluofzrmkoznskamwkxg.supabase.co', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhsdW9menJta296bnNrYW13a3hnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjU0ODYzMzAsImV4cCI6MjA0MTA2MjMzMH0.Y4uKt_QoE6me4y1EqOaJbYGvdEdPkX3QH3pfPN_tPDE')


export function HomePage() {

    const [uniqueShelves, setUniqueShelves] = useState<number | null>(null);
    const [totalShelfSearches, setTotalShelfSearches] = useState<number | null>(null);
    const [totalLibrarySearches, setTotalLibrarySearches] = useState<number | null>(null);
    const [totalLibraryAvailRate, setTotalLibraryAvailRate] = useState<number | null>(null);
    const [trendControl, setTrendControl] = useState('Daily');
    const [cumulativeShelfCountsData, setCumulativeShelfCountsData] = useState<any[] | null>(null);
    const [libraryAvailByMediumData, setLibraryAvailByMediumData] = useState<any[] | null>(null);
    const [hourlyShelfSearchesData, setHourlyShelfSearchesData] = useState<any[] | null>(null);
    const [totalsLoading, setTotalsLoading] = useState(true);
    const [trendsLoading, setTrendsLoading] = useState(true);



    useEffect(() => {
        // This is the initial data fetch for the initial state (Daily Trends to start)
        // Also includes the total numbers or anything that should only be pulled once
        const fetchData = async () => {
            console.log("Fetching Data...")
            try {
                const [
                    shelvesResponse,
                    shelfSearchesResponse,
                    librarySearchesResponse,
                    libraryAvailResponse,
                    cumulativeShelfDataResponse,
                    libraryAvailByMediumDataResponse,
                    hourlyShelfSearchesDataResponse,
                ] = await Promise.all([
                    supabase.from('total_unique_shelves').select('*').single(),
                    supabase.from('total_shelf_searches').select('*').single(),
                    supabase.from('total_library_searches').select('*').single(),
                    supabase.from('library_avail_rate').select('*').single(),
                    supabase.from('cumulative_shelf_counts_daily').select('*'),
                    supabase.from('library_availability_by_medium').select('*'),
                    supabase.from('hourly_shelf_searches').select('*'),
                ]);

                if (shelvesResponse.error) throw shelvesResponse.error
                if (shelfSearchesResponse.error) throw shelfSearchesResponse.error
                if (librarySearchesResponse.error) throw librarySearchesResponse.error
                if (libraryAvailResponse.error) throw libraryAvailResponse.error
                if (cumulativeShelfDataResponse.error) throw cumulativeShelfDataResponse.error
                if (libraryAvailByMediumDataResponse.error) throw libraryAvailByMediumDataResponse.error
                if (hourlyShelfSearchesDataResponse.error) throw hourlyShelfSearchesDataResponse.error
                setUniqueShelves(shelvesResponse.data.count)
                setTotalShelfSearches(shelfSearchesResponse.data.count)
                setTotalLibrarySearches(librarySearchesResponse.data.count)
                setTotalLibraryAvailRate(libraryAvailResponse.data.availability_perc)
                setCumulativeShelfCountsData(cumulativeShelfDataResponse.data)
                setLibraryAvailByMediumData(libraryAvailByMediumDataResponse.data)
                setHourlyShelfSearchesData(hourlyShelfSearchesDataResponse.data)

            } catch (error) {
                console.log('Error fetching data', error)
            } finally {
                setTotalsLoading(false)
                setTrendsLoading(false)
            }
        };
        fetchData();
    }, []);

    async function updateTrendCharts(trendLevel: string) {
        setTrendsLoading(true)
        setTrendControl(trendLevel)

        if (trendLevel == 'Daily') {
            await queryTrendData(setCumulativeShelfCountsData, setTrendsLoading, "cumulative_shelf_counts_daily");
        }
        else if (trendLevel == 'Weekly') {
            await queryTrendData(setCumulativeShelfCountsData, setTrendsLoading, "cumulative_shelf_counts_weekly");
        } else if (trendLevel == 'Monthly') {
            await queryTrendData(setCumulativeShelfCountsData, setTrendsLoading, "cumulative_shelf_counts_monthly");
        }
    }

    return (
        <AppShell header={{ height: 60, offset: false }} padding="md">
            <AppShell.Header>
                <HeaderSimple />
            </AppShell.Header>
            <AppShell.Main pt={`calc(${rem(60)} + var(--mantine-spacing-md))`}>
                <Container>
                    <SimpleGrid cols={2}>
                        <Skeleton visible={totalsLoading}>
                           <NumberIndicator title="Unique Shelves" value={uniqueShelves}/>
                        </Skeleton>
                        <Skeleton visible={totalsLoading}>
                            <NumberIndicator title='Total Searches' value={totalShelfSearches} />
                        </Skeleton>
                    </SimpleGrid>
                    <br></br>
                    <SimpleGrid cols={2}>
                    <Skeleton visible={totalsLoading}>
                           <NumberIndicator title="Library Searches" value={totalLibrarySearches}/>
                        </Skeleton>
                        <Skeleton visible={totalsLoading}>
                            <NumberIndicator title='Library Availability' value={totalLibraryAvailRate} suffix={"%"} />
                        </Skeleton>
                    </SimpleGrid>
                    <br></br>
                    <SimpleGrid cols={1}>
                    <SegmentedControl value={trendControl} onChange={updateTrendCharts} data={['Daily', 'Weekly', 'Monthly']} />
                    </SimpleGrid>
                    <br></br>
                    <Skeleton visible={trendsLoading}>
                       <AreaChartCard 
                        data={cumulativeShelfCountsData}
                        title="Cumulative Total of Unique Shelves"
                        loading={trendsLoading}
                        yAxisLimit={uniqueShelves ? uniqueShelves + 5 : 10}
                       />
                    </Skeleton>
                    <br></br>
                    <Skeleton visible={totalsLoading}>
                        <BarChartCard
                         data={libraryAvailByMediumData}
                         title="Library Availability by Medium"
                         loading={totalsLoading}
                        />
                    </Skeleton>
                    <br></br>
                    <Skeleton visible={totalsLoading}>
                        <HourlyBarChartCard
                            data={hourlyShelfSearchesData}
                            title="Shelf Searches by Hour"
                            loading={totalsLoading}
                        />
                    </Skeleton>
                </Container>
            </AppShell.Main>
        </AppShell>
    )
}

async function queryTrendData(
    setCumulativeShelfCountsData: { (value: SetStateAction<any[] | null>): void; (arg0: { cumulative_shelf_count: number | null; date: string | null; date_axis: string | null; shelf_count: number | null; }[]): void; },
    setTrendsLoading: { (value: SetStateAction<boolean>): void; (arg0: boolean): void; },
    tableName: "cumulative_shelf_counts_daily" | "cumulative_shelf_counts_monthly" | "cumulative_shelf_counts_weekly" | "total_shelf_searches" | "total_unique_shelves") {
    try {
        const [
            cumulativeShelfDataResponse
        ] = await Promise.all([
            supabase.from(tableName).select('*')
        ]);
        if (cumulativeShelfDataResponse.error) throw cumulativeShelfDataResponse.error;
        setCumulativeShelfCountsData(cumulativeShelfDataResponse.data);
    } catch (error) {
        console.log('Error fetching data', error);
    } finally {
        setTrendsLoading(false);
    }
}
