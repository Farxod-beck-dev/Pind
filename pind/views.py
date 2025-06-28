from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Note
from .forms import NoteForm

@login_required
def note_list(request):
    notes = Note.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'pind/note_list.html', {'notes': notes})

@login_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'pind/note_form.html', {'form': form})

@login_required
def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'pind/note_form.html', {'form': form})

@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'pind/note_confirm_delete.html', {'note': note})
@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    comments = note.comments.order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.note = note
            comment.user = request.user
            comment.save()
            return redirect('note_detail', pk=note.pk)
    else:
        form = CommentForm()

    return render(request, 'pind/note_detail.html', {
        'note': note,
        'comments': comments,
        'form': form
    })

from .models import Favorite

@login_required
def toggle_favorite(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    favorite, created = Favorite.objects.get_or_create(user=request.user, note=note)
    if not created:
        favorite.delete()
    return redirect('note_list')

from django.db.models import Q

@login_required
def search_notes(request):
    query = request.GET.get('q', '')
    results = Note.objects.filter(
        Q(user=request.user),  # faqat o‘z notelari
        Q(title__icontains=query) | Q(content__icontains=query)
    )
    return render(request, 'notes/search_results.html', {'notes': results, 'query': query})
