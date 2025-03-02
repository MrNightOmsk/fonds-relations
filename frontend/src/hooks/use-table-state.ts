import { useCallback, useEffect, useState } from "react"
import { useRouter, useSearchParams } from "next/navigation"
import { SortingState, ColumnFiltersState } from "@tanstack/react-table"

interface TableState {
  sorting: SortingState
  columnFilters: ColumnFiltersState
  pageIndex: number
  pageSize: number
}

export function useTableState(defaultPageSize: number = 10) {
  const router = useRouter()
  const searchParams = useSearchParams()

  const [state, setState] = useState<TableState>(() => {
    const sorting = searchParams.get("sort")
      ? (JSON.parse(searchParams.get("sort")!) as SortingState)
      : []
    const columnFilters = searchParams.get("filters")
      ? (JSON.parse(searchParams.get("filters")!) as ColumnFiltersState)
      : []
    const pageIndex = searchParams.get("page")
      ? parseInt(searchParams.get("page")!)
      : 0
    const pageSize = searchParams.get("size")
      ? parseInt(searchParams.get("size")!)
      : defaultPageSize

    return {
      sorting,
      columnFilters,
      pageIndex,
      pageSize,
    }
  })

  const updateUrl = useCallback(
    (newState: Partial<TableState>) => {
      const updatedState = { ...state, ...newState }
      const params = new URLSearchParams()

      if (updatedState.sorting.length > 0) {
        params.set("sort", JSON.stringify(updatedState.sorting))
      }
      if (updatedState.columnFilters.length > 0) {
        params.set("filters", JSON.stringify(updatedState.columnFilters))
      }
      if (updatedState.pageIndex > 0) {
        params.set("page", updatedState.pageIndex.toString())
      }
      if (updatedState.pageSize !== defaultPageSize) {
        params.set("size", updatedState.pageSize.toString())
      }

      const search = params.toString()
      const query = search ? `?${search}` : ""
      router.push(query)
    },
    [state, router, defaultPageSize]
  )

  const setSorting = useCallback(
    (sorting: SortingState) => {
      setState((prev) => ({ ...prev, sorting }))
      updateUrl({ sorting })
    },
    [updateUrl]
  )

  const setColumnFilters = useCallback(
    (columnFilters: ColumnFiltersState) => {
      setState((prev) => ({ ...prev, columnFilters }))
      updateUrl({ columnFilters })
    },
    [updateUrl]
  )

  const setPageIndex = useCallback(
    (pageIndex: number) => {
      setState((prev) => ({ ...prev, pageIndex }))
      updateUrl({ pageIndex })
    },
    [updateUrl]
  )

  const setPageSize = useCallback(
    (pageSize: number) => {
      setState((prev) => ({ ...prev, pageSize, pageIndex: 0 }))
      updateUrl({ pageSize, pageIndex: 0 })
    },
    [updateUrl]
  )

  return {
    ...state,
    setSorting,
    setColumnFilters,
    setPageIndex,
    setPageSize,
  }
} 