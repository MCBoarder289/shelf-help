export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  public: {
    Tables: {
      atlas_schema_revisions: {
        Row: {
          applied: number
          description: string
          error: string | null
          error_stmt: string | null
          executed_at: string
          execution_time: number
          hash: string
          operator_version: string
          partial_hashes: Json | null
          total: number
          type: number
          version: string
        }
        Insert: {
          applied?: number
          description: string
          error?: string | null
          error_stmt?: string | null
          executed_at: string
          execution_time: number
          hash: string
          operator_version: string
          partial_hashes?: Json | null
          total?: number
          type?: number
          version: string
        }
        Update: {
          applied?: number
          description?: string
          error?: string | null
          error_stmt?: string | null
          executed_at?: string
          execution_time?: number
          hash?: string
          operator_version?: string
          partial_hashes?: Json | null
          total?: number
          type?: number
          version?: string
        }
        Relationships: []
      }
      books: {
        Row: {
          author: string | null
          book_id: number
          date_added: string | null
          date_last_displayed: string | null
          gr_id: number | null
          isbn: string | null
          title: string | null
          unique_hash: string
        }
        Insert: {
          author?: string | null
          book_id?: never
          date_added?: string | null
          date_last_displayed?: string | null
          gr_id?: number | null
          isbn?: string | null
          title?: string | null
          unique_hash: string
        }
        Update: {
          author?: string | null
          book_id?: never
          date_added?: string | null
          date_last_displayed?: string | null
          gr_id?: number | null
          isbn?: string | null
          title?: string | null
          unique_hash?: string
        }
        Relationships: []
      }
      libraries: {
        Row: {
          library_id: string
          library_name: string
        }
        Insert: {
          library_id: string
          library_name: string
        }
        Update: {
          library_id?: string
          library_name?: string
        }
        Relationships: []
      }
      library_searches: {
        Row: {
          availability_message: string | null
          available: boolean | null
          book_id: number | null
          is_libby: boolean | null
          library_id: string
          library_search_id: number
          time_complete: string | null
          time_start: string | null
        }
        Insert: {
          availability_message?: string | null
          available?: boolean | null
          book_id?: number | null
          is_libby?: boolean | null
          library_id: string
          library_search_id?: never
          time_complete?: string | null
          time_start?: string | null
        }
        Update: {
          availability_message?: string | null
          available?: boolean | null
          book_id?: number | null
          is_libby?: boolean | null
          library_id?: string
          library_search_id?: never
          time_complete?: string | null
          time_start?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "library_searches_book_id_fkey"
            columns: ["book_id"]
            isOneToOne: false
            referencedRelation: "books"
            referencedColumns: ["book_id"]
          },
          {
            foreignKeyName: "library_searches_library_id_fkey"
            columns: ["library_id"]
            isOneToOne: false
            referencedRelation: "libraries"
            referencedColumns: ["library_id"]
          },
        ]
      }
      shelf_searches: {
        Row: {
          books_returned: number[] | null
          num_books: number | null
          search_type: string | null
          shelf_id: number | null
          shelf_search_id: number
          time_complete: string | null
          time_start: string | null
          total_book_count: number | null
        }
        Insert: {
          books_returned?: number[] | null
          num_books?: number | null
          search_type?: string | null
          shelf_id?: number | null
          shelf_search_id?: never
          time_complete?: string | null
          time_start?: string | null
          total_book_count?: number | null
        }
        Update: {
          books_returned?: number[] | null
          num_books?: number | null
          search_type?: string | null
          shelf_id?: number | null
          shelf_search_id?: never
          time_complete?: string | null
          time_start?: string | null
          total_book_count?: number | null
        }
        Relationships: [
          {
            foreignKeyName: "shelf_searches_shelf_id_fkey"
            columns: ["shelf_id"]
            isOneToOne: false
            referencedRelation: "shelves"
            referencedColumns: ["shelf_id"]
          },
        ]
      }
      shelves: {
        Row: {
          date_added: string | null
          date_last_searched: string | null
          shelf_id: number
          shelf_url: string
        }
        Insert: {
          date_added?: string | null
          date_last_searched?: string | null
          shelf_id?: never
          shelf_url: string
        }
        Update: {
          date_added?: string | null
          date_last_searched?: string | null
          shelf_id?: never
          shelf_url?: string
        }
        Relationships: []
      }
    }
    Views: {
      cumulative_shelf_counts_daily: {
        Row: {
          "Cumulative Shelf Count": number | null
          date: string | null
          date_axis: string | null
          shelf_count: number | null
        }
        Relationships: []
      }
      cumulative_shelf_counts_monthly: {
        Row: {
          "Cumulative Shelf Count": number | null
          date: string | null
          date_axis: string | null
          shelf_count: number | null
        }
        Relationships: []
      }
      cumulative_shelf_counts_weekly: {
        Row: {
          "Cumulative Shelf Count": number | null
          date: string | null
          date_axis: string | null
          shelf_count: number | null
        }
        Relationships: []
      }
      hourly_shelf_searches: {
        Row: {
          Hour: number | null
          Searches: number | null
        }
        Relationships: []
      }
      library_avail_rate: {
        Row: {
          availability_perc: number | null
        }
        Relationships: []
      }
      library_availability_by_medium: {
        Row: {
          Available: number | null
          medium: string | null
          Unavailable: number | null
        }
        Relationships: []
      }
      search_type_summary: {
        Row: {
          color: string | null
          name: string | null
          value: number | null
        }
        Relationships: []
      }
      total_library_searches: {
        Row: {
          count: number | null
        }
        Relationships: []
      }
      total_shelf_searches: {
        Row: {
          count: number | null
        }
        Relationships: []
      }
      total_unique_shelves: {
        Row: {
          count: number | null
        }
        Relationships: []
      }
    }
    Functions: {
      [_ in never]: never
    }
    Enums: {
      [_ in never]: never
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

type PublicSchema = Database[Extract<keyof Database, "public">]

export type Tables<
  PublicTableNameOrOptions extends
    | keyof (PublicSchema["Tables"] & PublicSchema["Views"])
    | { schema: keyof Database },
  TableName extends PublicTableNameOrOptions extends { schema: keyof Database }
    ? keyof (Database[PublicTableNameOrOptions["schema"]]["Tables"] &
        Database[PublicTableNameOrOptions["schema"]]["Views"])
    : never = never,
> = PublicTableNameOrOptions extends { schema: keyof Database }
  ? (Database[PublicTableNameOrOptions["schema"]]["Tables"] &
      Database[PublicTableNameOrOptions["schema"]]["Views"])[TableName] extends {
      Row: infer R
    }
    ? R
    : never
  : PublicTableNameOrOptions extends keyof (PublicSchema["Tables"] &
        PublicSchema["Views"])
    ? (PublicSchema["Tables"] &
        PublicSchema["Views"])[PublicTableNameOrOptions] extends {
        Row: infer R
      }
      ? R
      : never
    : never

export type TablesInsert<
  PublicTableNameOrOptions extends
    | keyof PublicSchema["Tables"]
    | { schema: keyof Database },
  TableName extends PublicTableNameOrOptions extends { schema: keyof Database }
    ? keyof Database[PublicTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = PublicTableNameOrOptions extends { schema: keyof Database }
  ? Database[PublicTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Insert: infer I
    }
    ? I
    : never
  : PublicTableNameOrOptions extends keyof PublicSchema["Tables"]
    ? PublicSchema["Tables"][PublicTableNameOrOptions] extends {
        Insert: infer I
      }
      ? I
      : never
    : never

export type TablesUpdate<
  PublicTableNameOrOptions extends
    | keyof PublicSchema["Tables"]
    | { schema: keyof Database },
  TableName extends PublicTableNameOrOptions extends { schema: keyof Database }
    ? keyof Database[PublicTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = PublicTableNameOrOptions extends { schema: keyof Database }
  ? Database[PublicTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Update: infer U
    }
    ? U
    : never
  : PublicTableNameOrOptions extends keyof PublicSchema["Tables"]
    ? PublicSchema["Tables"][PublicTableNameOrOptions] extends {
        Update: infer U
      }
      ? U
      : never
    : never

export type Enums<
  PublicEnumNameOrOptions extends
    | keyof PublicSchema["Enums"]
    | { schema: keyof Database },
  EnumName extends PublicEnumNameOrOptions extends { schema: keyof Database }
    ? keyof Database[PublicEnumNameOrOptions["schema"]]["Enums"]
    : never = never,
> = PublicEnumNameOrOptions extends { schema: keyof Database }
  ? Database[PublicEnumNameOrOptions["schema"]]["Enums"][EnumName]
  : PublicEnumNameOrOptions extends keyof PublicSchema["Enums"]
    ? PublicSchema["Enums"][PublicEnumNameOrOptions]
    : never
