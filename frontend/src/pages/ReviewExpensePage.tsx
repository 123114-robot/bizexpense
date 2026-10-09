import { useNavigate } from 'react-router-dom'
import { ExpenseForm } from '../components/forms/ExpenseForm'
import { expenseService } from '../services/expenseService'
import type { ExpenseInput, OCRResult } from '../types/expense'

const confidenceLabels: Record<string, string> = {
  supplier_name: 'Supplier',
  abn: 'ABN',
  invoice_number: 'Invoice number',
  invoice_date: 'Invoice date',
  due_date: 'Due date',
  subtotal: 'Subtotal',
  gst: 'GST',
  total: 'Total',
  currency: 'Currency',
}

export function ReviewExpensePage() {
  const navigate = useNavigate()
  const raw = sessionStorage.getItem('ocrDraft')
  const draft = raw ? JSON.parse(raw) as OCRResult & { document_id: number } : null
  if (!draft) return <p>No extracted invoice is ready for review.</p>

  const lowConfidenceFields = Object.entries(draft.field_confidence ?? {})
    .filter(([, confidence]) => confidence < 0.7)
    .map(([field, confidence]) => `${confidenceLabels[field] ?? field} (${Math.round(confidence * 100)}%)`)
  const initial: Partial<ExpenseInput> = {
    supplier_name: draft.supplier_name,
    category_id: 1,
    document_id: draft.document_id,
    invoice_number: draft.invoice_number,
    invoice_date: draft.invoice_date,
    due_date: draft.due_date,
    subtotal: String(draft.subtotal),
    gst_amount: String(draft.gst),
    total_amount: String(draft.total),
    currency: draft.currency,
    description: 'Uploaded invoice',
    ocr_confidence: draft.confidence,
    ocr_confirmed: false,
  }
  const save = async (data: ExpenseInput) => {
    const result = await expenseService.create(data)
    sessionStorage.removeItem('ocrDraft')
    navigate(`/expenses/${result.id}`)
  }

  return <>
    <h1 className="mb-1 text-3xl font-bold">Review expense</h1>
    <p className="mb-3 rounded-lg bg-amber-50 p-3 text-amber-900">Review extracted information before saving.</p>
    {lowConfidenceFields.length > 0 && <p className="mb-6 rounded-lg bg-rose-50 p-3 text-rose-900" role="status">
      Check low-confidence fields: {lowConfidenceFields.join(', ')}.
    </p>}
    <ExpenseForm initial={initial} onSubmit={save} submitLabel="Confirm and save" requireConfirmation />
  </>
}
