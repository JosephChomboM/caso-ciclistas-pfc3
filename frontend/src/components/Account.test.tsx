import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { expect, it, vi } from 'vitest'
import Account from './Account'
import { api } from '../api/client'

vi.mock('../api/client', () => ({ api: vi.fn(), session: { set: vi.fn() } }))
it('allows registration and then authenticates before reading the profile', async () => {
  const onUser = vi.fn()
  vi.mocked(api).mockResolvedValueOnce({}).mockResolvedValueOnce({ access_token: 'session' })
    .mockResolvedValueOnce({ id: 1, alias: 'Ana', role: 'cyclist' })
  render(<Account user={null} onUser={onUser} />)
  fireEvent.click(screen.getByText('Quiero crear una cuenta'))
  fireEvent.change(screen.getByLabelText('Cómo te llamamos'), { target: { value: 'Ana' } })
  fireEvent.change(screen.getByLabelText('Correo electrónico'), { target: { value: 'ana@example.com' } })
  fireEvent.change(screen.getByLabelText(/Contraseña/), { target: { value: 'A-long-password' } })
  fireEvent.click(screen.getByRole('button', { name: 'Crear cuenta' }))
  await waitFor(() => expect(onUser).toHaveBeenCalledWith(expect.objectContaining({ alias: 'Ana' })))
  expect(vi.mocked(api).mock.calls.map(x => x[0])).toEqual(['/users/register', '/users/login', '/users/me'])
})
