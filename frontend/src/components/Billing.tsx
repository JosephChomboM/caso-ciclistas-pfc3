import { useEffect, useState } from "react";
import { api, downloadFavorites, type User } from "../api/client";
import { dateInLima } from "../lib/time";

type Plan = {
  code: string;
  name: string;
  amount_centavos: number;
  features: string[];
};
type Invoice = {
  id: number;
  plan_code: string;
  amount_centavos: number;
  created_at: string;
  status: string;
};
type Subscription = { plan_code: string; mode: string };
const money = (centavos: number) =>
  new Intl.NumberFormat("es-PE", { style: "currency", currency: "PEN" }).format(
    centavos / 100,
  );

export default function Billing({
  user,
  onLogin,
}: {
  user: User | null;
  onLogin: () => void;
}) {
  const [plans, setPlans] = useState<Plan[]>([]);
  const [subscription, setSubscription] = useState<Subscription | null>(null);
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [busy, setBusy] = useState(true);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [attempt, setAttempt] = useState(0);
  useEffect(() => {
    let active = true;
    setBusy(true);
    setError("");
    setSubscription(null);
    setInvoices([]);
    Promise.all([
      api<{ plans: Plan[] }>("/billing/plans"),
      user ? api<Subscription>("/billing/subscription") : Promise.resolve(null),
      user ? api<Invoice[]>("/billing/invoices") : Promise.resolve([]),
    ])
      .then(([catalog, current, history]) => {
        if (active) {
          setPlans(catalog.plans);
          setSubscription(current);
          setInvoices(history);
        }
      })
      .catch((e) => {
        if (active) setError(e.message);
      })
      .finally(() => {
        if (active) setBusy(false);
      });
    return () => {
      active = false;
    };
  }, [user?.id, attempt]);
  async function changePlan(plan: Plan) {
    if (!user) {
      onLogin();
      return;
    }
    setBusy(true);
    setError("");
    setMessage("");
    try {
      setSubscription(
        await api<Subscription>("/billing/subscription", {
          method: "PUT",
          body: JSON.stringify({ plan_code: plan.code }),
        }),
      );
      setInvoices(await api<Invoice[]>("/billing/invoices"));
      setMessage(
        `Cambiaste a ${plan.name}. Es una simulación: no se realizó ningún cobro.`,
      );
    } catch (e) {
      setError(e instanceof Error ? e.message : "No se pudo cambiar de plan.");
    } finally {
      setBusy(false);
    }
  }
  async function download() {
    setBusy(true);
    setError("");
    try {
      await downloadFavorites();
      setMessage("Se descargó el CSV con tus favoritos.");
    } catch (e) {
      setError(
        e instanceof Error
          ? e.message
          : "No se pudo descargar. Inténtalo otra vez.",
      );
    } finally {
      setBusy(false);
    }
  }
  return (
    <section className="form-panel billing-panel">
      <h2>Planes para seguir pedaleando</h2>
      <p>
        Prueba cómo funcionaría una suscripción de CicloLima. Todos los importes
        y comprobantes de esta página son de demostración: no se solicitan
        tarjetas ni se realizan cobros.
      </p>
      {error && (
        <div role="alert" className="form-message">
          <p>{error}</p>
          <button disabled={busy} onClick={() => setAttempt((x) => x + 1)}>
            Volver a cargar
          </button>
        </div>
      )}
      {message && (
        <p role="status" className="form-message">
          {message}
        </p>
      )}
      {busy && plans.length === 0 && <p role="status">Cargando planes…</p>}
      <div className="plan-options">
        {plans.map((plan) => (
          <article key={plan.code}>
            <h3>{plan.name}</h3>
            <p className="plan-price">
              {money(plan.amount_centavos)} <span>/ mes de referencia</span>
            </p>
            <ul>
              {plan.features.map((feature) => (
                <li key={feature}>{feature}</li>
              ))}
            </ul>
            <button
              className="primary"
              disabled={busy || subscription?.plan_code === plan.code}
              onClick={() => changePlan(plan)}
            >
              {subscription?.plan_code === plan.code
                ? "Tu plan actual"
                : user
                  ? `Probar ${plan.name}`
                  : "Ingresar para probar"}
            </button>
          </article>
        ))}
      </div>
      {user && subscription?.plan_code === "plus" && (
        <div className="export-favorites">
          <h3>Lleva tus lugares contigo</h3>
          <p>
            Descarga tus estacionamientos favoritos en un archivo CSV con su
            fuente.
          </p>
          <button disabled={busy} onClick={download}>
            Exportar mis favoritos
          </button>
        </div>
      )}
      {user && (
        <section className="invoice-history">
          <h3>Tus comprobantes de demostración</h3>
          {invoices.length === 0 ? (
            <p>
              Aún no tienes comprobantes. Aparecerán al probar un cambio de
              plan.
            </p>
          ) : (
            <div className="table-scroll">
              <table>
                <caption>
                  Historial privado de cambios de plan. Ningún registro acredita
                  un pago.
                </caption>
                <thead>
                  <tr>
                    <th>Referencia</th>
                    <th>Fecha</th>
                    <th>Plan</th>
                    <th>Importe simulado</th>
                    <th>Estado</th>
                  </tr>
                </thead>
                <tbody>
                  {invoices.map((invoice) => (
                    <tr key={invoice.id}>
                      <td>DEMO-{invoice.id}</td>
                      <td>{dateInLima(invoice.created_at)}</td>
                      <td>
                        {invoice.plan_code === "plus" ? "Plus" : "Comunidad"}
                      </td>
                      <td>{money(invoice.amount_centavos)}</td>
                      <td>Simulado</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      )}
    </section>
  );
}
