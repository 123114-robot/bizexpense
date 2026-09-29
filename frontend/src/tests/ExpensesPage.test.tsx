import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { vi } from 'vitest'

import { ExpensesPage } from '../pages/ExpensesPage'

afterEach(() => vi.unstubAllGlobals())

test('expense filters drive both the list and CSV export', async () => {
  const fetchMock = vi.fn().mockImplementation((url: string) =>
    Promise.resolve({
      ok: true,
      json: async () => url.includes('/categories')
        ? [{ id: 2, name: 'Fuel' }]
        : [],
    }),
  )
  vi.stubGlobal('fetch', fetchMock)

  render(<MemoryRouter><ExpensesPage /></MemoryRouter>)

  await userEvent.selectOptions(await screen.findByLabelText('Category'), '2')
  await userEvent.selectOptions(screen.getByLabelText('Status'), 'true')
  await userEvent.type(screen.getByLabelText('From date'), '2026-09-01')
  await userEvent.type(screen.getByLabelText('To date'), '2026-09-30')

  const exportLink = screen.getByRole('link', { name: 'Export CSV' })
  expect(exportLink).toHaveAttribute(
    'href',
    '/api/expenses/export.csv?category_id=2&date_from=2026-09-01&date_to=2026-09-30&ocr_confirmed=true',
  )
  await waitFor(() => expect(fetchMock).toHaveBeenCalledWith(
    '/api/expenses?category_id=2&date_from=2026-09-01&date_to=2026-09-30&ocr_confirmed=true',
    undefined,
  ))
})
