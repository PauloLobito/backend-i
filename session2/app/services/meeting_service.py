from app.domain.models import Meeting
from app.services.memory_store import meetings


def add_meeting(meeting: Meeting) -> None:
    meetings.append(meeting)


def list_meetings() -> str:
    if not meetings:
        return "Nenhuma reunião encontrada."

    linhas: list[str] = []

    for meeting in meetings:
        participantes = ", ".join(meeting.participants) if meeting.participants else "Nenhum"

        linhas.append(f"Reunião: {meeting.title} ({meeting.id})")
        linhas.append(f"  Data: {meeting.date}")
        linhas.append(f"  Responsável: {meeting.owner}")
        linhas.append(f"  Participantes: {participantes}")
        linhas.append(f"  Total de tarefas: {meeting.task_count}")

        if meeting.action_items:
            linhas.append("  Tarefas:")
            for i, item in enumerate(meeting.action_items, start=1):
                linhas.append(
                    f"    {i}. {item.description} | responsável={item.owner} | prazo={item.due_date} | status={item.status}"
                )
        else:
            linhas.append("  Tarefas: Nenhuma")

        linhas.append("")

    return "\n".join(linhas).strip()