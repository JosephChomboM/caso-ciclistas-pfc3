import { useState, type FormEvent } from 'react'
import { api, session, type User } from '../api/client'

export default function Account({ user, onUser }: { user: User | null; onUser: (user: User | null) => void }) {
  const [register, setRegister] = useState(false)
  const [busy, setBusy] = useState(false)
  const [message, setMessage] = useState('')
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setBusy(true); setMessage('')
    const form = new FormData(event.currentTarget)
    try {
      if (user) {
        onUser(await api<User>('/users/me', { method: 'PATCH', body: JSON.stringify({
          alias: form.get('alias'), district: form.get('district'),
        }) })); setMessage('Tus preferencias se guardaron.')
      } else {
        const data = { email: form.get('email'), password: form.get('password') }
        if (register) await api('/users/register', { method: 'POST', body: JSON.stringify({ ...data, alias: form.get('alias') }) })
        const result = await api<{access_token: string}>('/users/login', { method: 'POST', body: JSON.stringify(data) })
        session.set(result.access_token)
        onUser(await api<User>('/users/me'))
      }
    } catch (error) { setMessage(error instanceof Error ? error.message : 'No se pudo guardar.') }
    finally { setBusy(false) }
  }
  async function logout() {
    setBusy(true); setMessage('')
    try { await api('/users/logout', { method: 'POST' }); session.set(null); onUser(null) }
    catch (error) { setMessage(error instanceof Error ? error.message : 'No se pudo cerrar la sesión.') }
    finally { setBusy(false) }
  }
  return <section className="form-panel"><h2>{user ? 'Tu perfil' : register ? 'Crea tu cuenta' : 'Vuelve a pedalear con nosotros'}</h2>
    <p>{user ? `Sesión de ${user.email}` : 'Guarda tus lugares favoritos y aporta información sobre los recorridos.'}</p>
    <form onSubmit={submit}>
      {(register || user) && <label>Cómo te llamamos<input name="alias" minLength={2} maxLength={60} autoComplete="nickname" required defaultValue={user?.alias} /></label>}
      {user ? <label>Distrito de interés<select name="district" defaultValue={user.district}><option value="">Sin preferencia</option>{['Miraflores','San Isidro','Barranco'].map(x => <option key={x}>{x}</option>)}</select></label> : <>
        <label>Correo electrónico<input name="email" type="email" autoComplete="email" required maxLength={254} /></label>
        <label>Contraseña<input name="password" type="password" autoComplete={register ? 'new-password' : 'current-password'} required minLength={10} maxLength={128} /><small>Entre 10 y 128 caracteres.</small></label>
      </>}
      {message && <p role="status" className="form-message">{message}</p>}
      <button className="primary" disabled={busy}>{busy ? 'Un momento…' : user ? 'Guardar preferencias' : register ? 'Crear cuenta' : 'Iniciar sesión'}</button>
    </form>
    {user ? <button className="secondary" disabled={busy} onClick={logout}>Cerrar todas mis sesiones</button> : <button className="secondary" onClick={() => { setRegister(!register); setMessage('') }}>{register ? 'Ya tengo una cuenta' : 'Quiero crear una cuenta'}</button>}
  </section>
}
