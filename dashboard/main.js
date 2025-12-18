/**
 * Lianna's Training Dashboard
 * Main Application Logic
 */

// ===================================
// LIANNA'S PROFILE DATA
// ===================================

const LIANNA_PROFILE = {
    last_period_start: "2025-11-27",
    average_cycle_length: 28,
    name: "Lianna"
};

// ===================================
// DYNAMIC CYCLE PHASE CALCULATION
// ===================================

function calculateCyclePhase() {
    const lastPeriod = new Date(LIANNA_PROFILE.last_period_start);
    const today = new Date();
    const cycleLength = LIANNA_PROFILE.average_cycle_length;

    // Calculate days since last period started
    const daysSinceStart = Math.floor((today - lastPeriod) / (1000 * 60 * 60 * 24));

    // Account for multiple cycles (if more than one cycle has passed)
    const dayInCycle = (daysSinceStart % cycleLength) + 1;

    // Determine phase based on day
    let phase, energy, training_tip;

    if (dayInCycle <= 5) {
        phase = "Menstrual";
        energy = "Variable - listen to your body";
        training_tip = "Lighter weights OK. Focus on form. Rest if needed.";
    } else if (dayInCycle <= 14) {
        phase = "Follicular";
        energy = "HIGH - rising estrogen = strength gains!";
        training_tip = "BEST time for heavy lifts & PRs! Push hard, increase weights.";
    } else if (dayInCycle <= 17) {
        phase = "Ovulation";
        energy = "PEAK energy but injury risk higher";
        training_tip = "Strong lifts possible. Extra warm-up recommended.";
    } else {
        phase = "Luteal";
        energy = "Moderate - may feel more fatigued";
        training_tip = "Maintain volume but listen to body. Longer rest periods OK.";
    }

    return {
        phase,
        day: dayInCycle,
        energy,
        training_tip
    };
}

// ===================================
// SAMPLE DATA (Replace with API calls to Google Sheets)
// ===================================

const SAMPLE_WORKOUT_DATA = {
    coaching_notes: "This week focuses on progressive overload. I've programmed heavy compounds with isolation finishers to maximize your gains. Remember to adjust intensity based on how you're feeling!",
    current_week: 2,
    cycle_phase: calculateCyclePhase(), // Now calculated dynamically!
    Monday: [
        {
            category: "Glute_Compound_Heavy",
            exercise: "Barbell Hip Thrust",
            sets: 4,
            reps: "8-10",
            rest: "90s",
            target_weight: "145 lbs",
            url: "https://youtube.com/shorts/42lU8xsumBo",
            cues: "Drive through heels. Chin tucked. Full lockout at top."
        },
        {
            category: "Hinge_Pattern",
            exercise: "Romanian Deadlift",
            sets: 4,
            reps: "10-12",
            rest: "75s",
            target_weight: "105 lbs",
            url: "https://youtube.com/shorts/_TchJLlBO-4",
            cues: "Push hips back until hamstrings limit you. Soft knees."
        },
        {
            category: "Glute_Shortened_Iso",
            exercise: "Cable Kickbacks",
            sets: 3,
            reps: "12-15",
            rest: "60s",
            target_weight: "RPE 8",
            url: "https://youtube.com/shorts/n-cgsNePyFo",
            cues: "Do not rotate hips. Pure hip extension."
        },
        {
            category: "Hamstring_Lengthened",
            exercise: "Seated Leg Curl",
            sets: 3,
            reps: "10-12",
            rest: "60s",
            target_weight: "RPE 8",
            url: "https://youtube.com/shorts/Lh3iMIcbkBQ",
            cues: "Lean forward for stretch. Control the negative."
        },
        {
            category: "Unilateral_Leg",
            exercise: "B-Stance RDL",
            sets: 3,
            reps: "10 each side",
            rest: "60s",
            target_weight: "25 lb DBs",
            url: "https://www.youtube.com/shorts/qC0aLz61m9Y",
            cues: "90% load on working leg. Feel hamstring stretch."
        },
        {
            category: "Finisher",
            exercise: "Frog Pumps",
            sets: 2,
            reps: "25",
            rest: "45s",
            target_weight: "Bodyweight",
            url: "https://youtu.be/MQ62r2V7Lw8",
            cues: "Soles together. Squeeze glutes at top. BURN!"
        }
    ],
    Tuesday: [
        {
            category: "Vertical_Pull_Heavy",
            exercise: "Lat Pulldown (Wide Grip)",
            sets: 4,
            reps: "8-10",
            rest: "90s",
            target_weight: "80 lbs",
            url: "https://youtube.com/shorts/Oa1ta2lU3ZI",
            cues: "Pull elbows to pockets. Don't lean back too far."
        },
        {
            category: "Overhead_Press_Heavy",
            exercise: "Seated Dumbbell Press",
            sets: 4,
            reps: "8-10",
            rest: "90s",
            target_weight: "20 lbs each",
            url: "https://youtube.com/shorts/osEKVtXBLlU",
            cues: "Full ROM. Touch DBs to shoulders."
        },
        {
            category: "Horizontal_Row_Volume",
            exercise: "Chest Supported Row",
            sets: 3,
            reps: "10-12",
            rest: "60s",
            target_weight: "25 lb DBs",
            url: "https://youtube.com/shorts/czoQ_ncuqqI",
            cues: "Eliminate momentum. Isolate the back."
        },
        {
            category: "Lateral_Delt",
            exercise: "Cable Lateral Raises",
            sets: 3,
            reps: "12-15",
            rest: "60s",
            target_weight: "RPE 8",
            url: "https://youtube.com/shorts/xrBcuPNTxLg",
            cues: "Cross body for better stretch. Lead with elbows."
        },
        {
            category: "Tricep_Iso",
            exercise: "Tricep Rope Pushdowns",
            sets: 3,
            reps: "12-15",
            rest: "45s",
            target_weight: "RPE 8",
            url: "https://youtube.com/shorts/IKQ_bKGT3LQ",
            cues: "Spread rope at bottom. Keep elbows pinned."
        },
        {
            category: "Rear_Delt",
            exercise: "Face Pulls",
            sets: 3,
            reps: "15-20",
            rest: "45s",
            target_weight: "RPE 7",
            url: "https://youtube.com/shorts/8686PLZB_1Q",
            cues: "Pull to forehead. External rotation at end."
        }
    ],
    Wednesday: [
        {
            category: "Squat_Pattern_Heavy",
            exercise: "Smith Machine Squat",
            sets: 4,
            reps: "8-10",
            rest: "2 mins",
            target_weight: "95 lbs",
            url: "https://youtube.com/shorts/iKCJCydYYrE",
            cues: "Feet slightly forward. Keep torso upright."
        },
        {
            category: "Lunge_Pattern",
            exercise: "Walking Lunges",
            sets: 3,
            reps: "10 each leg",
            rest: "60s",
            target_weight: "20 lb DBs",
            url: "https://youtube.com/shorts/2ea3_b9rFdM",
            cues: "Slight forward lean. Drive off front heel."
        },
        {
            category: "Quad_Isolation_Shortened",
            exercise: "Leg Extensions",
            sets: 3,
            reps: "12-15",
            rest: "60s",
            target_weight: "RPE 8",
            url: "https://youtube.com/shorts/ztNBgrGy6FQ",
            cues: "Pause at the top. Squeeze quads hard."
        },
        {
            category: "Calves",
            exercise: "Standing Calf Raise",
            sets: 4,
            reps: "12-15",
            rest: "45s",
            target_weight: "RPE 8",
            url: "https://youtube.com/shorts/a-x_NR-ibos",
            cues: "Deep stretch at bottom. Pause 2s at peak."
        },
        {
            category: "Core_Stability",
            exercise: "Plank",
            sets: 3,
            reps: "45 seconds",
            rest: "30s",
            target_weight: "Bodyweight",
            url: "https://youtube.com/shorts/xe2MXatLTUw",
            cues: "Squeeze glutes. Don't let hips sag or pike."
        },
        {
            category: "Core_Rotation",
            exercise: "Cable Woodchoppers",
            sets: 3,
            reps: "12 each side",
            rest: "45s",
            target_weight: "RPE 7",
            url: "https://youtube.com/shorts/YIU0U_B57rU",
            cues: "Rotate through thoracic spine, not hips."
        }
    ],
    Thursday: [
        {
            category: "Horizontal_Push",
            exercise: "Incline Dumbbell Press",
            sets: 4,
            reps: "10-12",
            rest: "75s",
            target_weight: "22.5 lbs each",
            url: "https://www.youtube.com/watch?v=8iPEnn-ltC8",
            cues: "Focus on upper chest. 30 degree bench."
        },
        {
            category: "Bicep_Isolation",
            exercise: "Bayesian Curls",
            sets: 3,
            reps: "10-12",
            rest: "60s",
            target_weight: "RPE 8",
            url: "https://youtube.com/shorts/BaSd7C58L3o",
            cues: "Cable behind back. Maximal stretch on bicep."
        },
        {
            category: "Tricep_Overhead",
            exercise: "Overhead Cable Extension",
            sets: 3,
            reps: "12-15",
            rest: "60s",
            target_weight: "RPE 8",
            url: "https://youtube.com/shorts/9Ark9S11uXw",
            cues: "Stretch the long head. Keep elbows in."
        },
        {
            category: "Lateral_Delt",
            exercise: "Lu Raises",
            sets: 3,
            reps: "10-12",
            rest: "60s",
            target_weight: "8 lb DBs",
            url: "https://youtube.com/shorts/oZgHeEFY8pc",
            cues: "Full overhead range. Control eccentric."
        },
        {
            category: "Bicep_Hammer",
            exercise: "Hammer Curls",
            sets: 3,
            reps: "10-12",
            rest: "45s",
            target_weight: "15 lbs",
            url: "https://youtube.com/shorts/lmIo_gVE8T4",
            cues: "Neutral grip. Hits brachialis for arm width."
        },
        {
            category: "Core_Obliques",
            exercise: "Russian Twists",
            sets: 3,
            reps: "20 total",
            rest: "45s",
            target_weight: "10 lb DB",
            url: "https://youtube.com/shorts/-BzNffL_6YE",
            cues: "Slow and controlled. Feet up if possible."
        }
    ],
    Friday: [
        {
            category: "Glute_Bridge_Volume",
            exercise: "B-Stance Hip Thrust",
            sets: 4,
            reps: "12 each side",
            rest: "60s",
            target_weight: "105 lbs",
            url: "https://youtu.be/9rDq2uQdau0",
            cues: "90% load on working leg. Kickstand only."
        },
        {
            category: "Hinge_Unilateral",
            exercise: "Single Leg RDL",
            sets: 3,
            reps: "10 each leg",
            rest: "60s",
            target_weight: "25 lb DB",
            url: "https://youtube.com/shorts/Iq1LP6dnf1U",
            cues: "Use wall for balance if needed. Hips square."
        },
        {
            category: "Abductor_Iso",
            exercise: "Seated Abductor Machine",
            sets: 3,
            reps: "15-20",
            rest: "45s",
            target_weight: "RPE 9",
            url: "https://youtube.com/shorts/tu4o4quPv2k",
            cues: "Lean forward for glutes. Hold 1s at peak."
        },
        {
            category: "Vertical_Pull",
            exercise: "Straight Arm Pulldown",
            sets: 3,
            reps: "12-15",
            rest: "60s",
            target_weight: "RPE 8",
            url: "https://youtube.com/shorts/hAMcfubonDc",
            cues: "Keep elbows slightly bent but locked. Squeeze lats."
        },
        {
            category: "Rear_Delt",
            exercise: "Reverse Pec Deck",
            sets: 3,
            reps: "15-20",
            rest: "45s",
            target_weight: "RPE 8",
            url: "https://youtube.com/shorts/7tgx6QHB0-A",
            cues: "Push back of hands away. Don't squeeze early."
        },
        {
            category: "Glute_Burnout",
            exercise: "Cable Pull Through",
            sets: 2,
            reps: "15-20",
            rest: "45s",
            target_weight: "RPE 8",
            url: "https://youtube.com/shorts/d3sH6fbCBP0",
            cues: "Hip hinge. Squeeze glutes to stand. FINISHER!"
        }
    ]
};

const RECOVERY_DATA = {
    yoga_flows: [
        {
            name: "Morning Energize Flow",
            duration: "12 mins",
            url: "https://www.youtube.com/watch?v=4pKly2JojMw",
            description: "Wake up your body and mind - great for Follicular/Ovulation phase",
            exercises: ["Sun Salutation A", "Warrior I → II", "Triangle Pose", "Chair Pose", "Forward Fold"]
        },
        {
            name: "Evening Unwind",
            duration: "15 mins",
            url: "https://www.youtube.com/watch?v=v7AYKMP6rOE",
            description: "Gentle, restorative sequence to reduce stress and improve sleep",
            exercises: ["Child's Pose", "Supine Twist", "Happy Baby", "Legs Up Wall", "Corpse Pose"]
        },
        {
            name: "Deep Hip Opening",
            duration: "20 mins",
            url: "https://www.youtube.com/watch?v=Ho8-3wbys5E",
            description: "Target tight hips from sitting and training - great for rest days",
            exercises: ["Butterfly", "Low Lunge", "Lizard Pose", "Frog Pose", "Pigeon Pose"]
        }
    ],
    stretching: [
        {
            name: "Lower Body Cool Down",
            duration: "10 mins",
            description: "Essential stretches after leg day to improve recovery",
            exercises: [
                { name: "90/90 Hip Stretch", duration: "60s each side", url: "https://youtube.com/shorts/yjGjT7JYVR4", cues: "Keep chest tall, rotate towards front leg" },
                { name: "Pigeon Pose", duration: "90s each side", url: "https://youtube.com/shorts/FBRVZbLFzjk", cues: "Square hips, fold forward for deeper stretch" },
                { name: "Standing Quad Stretch", duration: "45s each side", url: "https://youtube.com/shorts/GKe7eTdQmzs", cues: "Squeeze glute, push hips forward" },
                { name: "Seated Forward Fold", duration: "60s", url: "https://youtube.com/shorts/1uR5F_l3hc", cues: "Hinge at hips, reach for toes" },
                { name: "Figure Four Hip Stretch", duration: "60s each side", url: "https://youtube.com/shorts/cC8YWopAEYg", cues: "Flex ankle, pull knee towards chest" }
            ]
        },
        {
            name: "Upper Body Cool Down",
            duration: "8 mins",
            description: "Release tension in shoulders, chest, and back",
            exercises: [
                { name: "Doorway Chest Stretch", duration: "45s each arm", url: "https://youtube.com/shorts/2x8cP3zMzlg", cues: "90 degree elbow, lean forward gently" },
                { name: "Cross-Body Shoulder Stretch", duration: "30s each arm", url: "https://youtube.com/shorts/WvmIQ9J5TzE", cues: "Pull arm across chest, keep shoulder down" },
                { name: "Overhead Tricep Stretch", duration: "30s each arm", url: "https://youtube.com/shorts/jqF8wrR5xko", cues: "Elbow points to ceiling, gentle press" },
                { name: "Cat-Cow Stretch", duration: "60s (10 reps)", url: "https://youtube.com/shorts/OqWybnAbTI8", cues: "Flow with breath, full spinal movement" },
                { name: "Thread the Needle", duration: "45s each side", url: "https://youtube.com/shorts/HoCN7Wq5pZo", cues: "Rotate through thoracic spine" }
            ]
        }
    ],
    rest_day: [
        { name: "20-30 min Walk", description: "Easy pace, preferably outdoors for fresh air" },
        { name: "15 min Foam Rolling", description: "Full body routine for muscle recovery", url: "https://www.youtube.com/watch?v=bxQ68D4YEFQ" },
        { name: "Epsom Salt Bath", description: "20 mins - magnesium helps muscle relaxation" },
        { name: "Meditation", description: "10-15 mins - great for stress relief", url: "https://www.youtube.com/watch?v=inpok4MKVLM" }
    ]
};

const NUTRITION_TARGETS = {
    calories: 1800,
    protein: 120,
    carbs: 180,
    fat: 60
};

// Garmin Recovery Data (will be fetched from API in production)
const GARMIN_RECOVERY_DATA = {
    date: new Date().toISOString().split('T')[0],
    sleep_score: 81,
    sleep_duration_hours: 7.7,
    sleep_quality: "Excellent",
    stress_level: null,
    body_battery_morning: 40,
    body_battery_current: 23,
    hrv_status: "BALANCED",
    recovery_ready: true,
    recovery_notes: []
};

// ===================================
// STATE
// ===================================

let state = {
    activeTab: 'workout',
    selectedDay: 'Monday',
    workoutData: SAMPLE_WORKOUT_DATA,
    completedExercises: new Set(),
    nutritionLog: {
        calories: 0,
        protein: 0,
        carbs: 0,
        fat: 0
    }
};

// ===================================
// DOM ELEMENTS
// ===================================

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => document.querySelectorAll(selector);

// ===================================
// INITIALIZATION
// ===================================

const GITHUB_DATA_URL = '/api/data';

async function fetchLiveData() {
    try {
        const response = await fetch(GITHUB_DATA_URL);
        if (response.ok) {
            const liveData = await response.json();

            // Update Garmin recovery data
            if (liveData.recovery) {
                GARMIN_RECOVERY_DATA.sleep_score = liveData.recovery.sleep_score;
                GARMIN_RECOVERY_DATA.sleep_duration_hours = liveData.recovery.sleep_hours;

                GARMIN_RECOVERY_DATA.sleep_quality = liveData.recovery.sleep_quality;
                GARMIN_RECOVERY_DATA.body_battery_current = liveData.recovery.body_battery;
                GARMIN_RECOVERY_DATA.hrv_status = liveData.recovery.hrv_status;
                GARMIN_RECOVERY_DATA.recovery_ready = liveData.recovery.recovery_ready;
            }

            // Update cycle phase if available
            if (liveData.cycle_phase) {
                state.workoutData.cycle_phase = liveData.cycle_phase;
            }

            // Update workouts if available
            if (liveData.workouts) {
                Object.keys(liveData.workouts).forEach(day => {
                    state.workoutData[day] = liveData.workouts[day];
                });
            }

            if (liveData.coaching_notes) {
                state.workoutData.coaching_notes = liveData.coaching_notes;
            }

            console.log('Live data loaded:', liveData.last_updated);

            // Re-render with live data
            renderCycleBadge();
            renderCoachingNotes();
            renderWorkoutList();
            renderProgressTab();
        }
    } catch (error) {
        console.log('Using cached data, live fetch failed:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initDaySelector();
    renderCycleBadge();
    renderCoachingNotes();
    renderWorkoutList();
    renderNutritionTab();
    renderRecoveryTab();
    renderProgressTab();
    initModal();
    initNutritionForm();

    // Fetch live data from GitHub
    fetchLiveData();
});

// ===================================
// TAB NAVIGATION
// ===================================

function initTabs() {
    $$('.nav-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            const tabId = tab.dataset.tab;

            // Update active tab button
            $$('.nav-tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            // Update active content
            $$('.tab-content').forEach(content => content.classList.remove('active'));
            $(`#${tabId}-tab`).classList.add('active');

            state.activeTab = tabId;
        });
    });
}

// ===================================
// DAY SELECTOR
// ===================================

function initDaySelector() {
    const container = $('#daySelector');
    const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
    const today = new Date().toLocaleDateString('en-US', { weekday: 'long' });

    container.innerHTML = days.map(day => {
        const isToday = day === today;
        const isActive = day === state.selectedDay;
        return `
      <button class="day-btn ${isActive ? 'active' : ''} ${isToday ? 'today' : ''}" data-day="${day}">
        ${day.substring(0, 3)}
      </button>
    `;
    }).join('');

    container.querySelectorAll('.day-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            $$('.day-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            state.selectedDay = btn.dataset.day;
            renderWorkoutList();
        });
    });
}

// ===================================
// CYCLE BADGE
// ===================================

function renderCycleBadge() {
    const badge = $('#cycleBadge');
    const { phase, day } = state.workoutData.cycle_phase;
    badge.textContent = `${phase} Day ${day}`;
    badge.className = `cycle-badge ${phase.toLowerCase()}`;
}

// ===================================
// COACHING NOTES
// ===================================

function renderCoachingNotes() {
    const container = $('#coachingNotes');
    let notesText = state.workoutData.coaching_notes;

    // Handle array of objects (from AI) or string
    if (Array.isArray(notesText)) {
        notesText = notesText.map(note =>
            typeof note === 'object' ? (note.exercise || note.text || JSON.stringify(note)) : note
        ).join(' ');
    } else if (typeof notesText === 'object') {
        notesText = notesText.exercise || notesText.text || JSON.stringify(notesText);
    }

    container.innerHTML = `
    <h4>🎯 Coach's Notes</h4>
    <p>${notesText || 'No coaching notes for this week.'}</p>
  `;
}

// ===================================
// WORKOUT LIST
// ===================================

function renderWorkoutList() {
    const container = $('#workoutList');
    const exercises = state.workoutData[state.selectedDay] || [];

    if (exercises.length === 0) {
        container.innerHTML = `
      <div class="empty-state">
        <p>No workout scheduled for ${state.selectedDay}</p>
      </div>
    `;
        return;
    }

    container.innerHTML = exercises.map((ex, index) => {
        const isDone = state.completedExercises.has(`${state.selectedDay}-${index}`);
        return `
      <div class="exercise-card ${isDone ? 'done' : ''}" data-day="${state.selectedDay}" data-index="${index}">
        <div class="exercise-header">
          <div>
            <div class="exercise-name">${ex.exercise}</div>
            <div class="exercise-category">${ex.category.replace(/_/g, ' ')}</div>
          </div>
        </div>
        <div class="exercise-details">
          <div class="detail-item">
            <span class="detail-value">${ex.sets}</span>
            <span class="detail-label">Sets</span>
          </div>
          <div class="detail-item">
            <span class="detail-value">${ex.reps}</span>
            <span class="detail-label">Reps</span>
          </div>
          <div class="detail-item">
            <span class="detail-value">${ex.target_weight}</span>
            <span class="detail-label">Weight</span>
          </div>
          <div class="detail-item">
            <span class="detail-value">${ex.rest}</span>
            <span class="detail-label">Rest</span>
          </div>
        </div>
        <div class="exercise-cues">"${ex.cues}"</div>
      </div>
    `;
    }).join('');

    // Add click handlers
    container.querySelectorAll('.exercise-card').forEach(card => {
        card.addEventListener('click', () => openExerciseModal(card.dataset.day, card.dataset.index));
    });
}

// ===================================
// MODAL
// ===================================

function initModal() {
    const modal = $('#exerciseModal');
    const closeBtn = $('#modalClose');
    const saveBtn = $('#saveLog');

    closeBtn.addEventListener('click', () => modal.classList.remove('active'));
    modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.classList.remove('active');
    });

    saveBtn.addEventListener('click', saveExerciseLog);
}

function openExerciseModal(day, index) {
    const exercise = state.workoutData[day][index];
    const modal = $('#exerciseModal');

    $('#modalTitle').textContent = exercise.exercise;
    $('#modalCues').textContent = exercise.cues;

    // Embed YouTube video
    const videoContainer = $('#modalVideo');
    const videoId = extractYouTubeId(exercise.url);
    if (videoId) {
        videoContainer.innerHTML = `
      <iframe 
        src="https://www.youtube.com/embed/${videoId}" 
        allowfullscreen
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture">
      </iframe>
    `;
    } else {
        videoContainer.innerHTML = `<a href="${exercise.url}" target="_blank" style="color: var(--primary-light); padding: 20px; display: block; text-align: center;">Watch Video ↗</a>`;
    }

    // Store current exercise reference
    modal.dataset.day = day;
    modal.dataset.index = index;

    // Clear form
    $('#logWeight').value = '';
    $('#logReps').value = '';
    $('#logRPE').value = '';

    modal.classList.add('active');
}

function extractYouTubeId(url) {
    const patterns = [
        /youtube\.com\/watch\?v=([^&]+)/,
        /youtube\.com\/shorts\/([^?]+)/,
        /youtu\.be\/([^?]+)/,
        /youtube\.com\/embed\/([^?]+)/
    ];

    for (const pattern of patterns) {
        const match = url.match(pattern);
        if (match) return match[1];
    }
    return null;
}

function saveExerciseLog() {
    const modal = $('#exerciseModal');
    const day = modal.dataset.day;
    const index = modal.dataset.index;

    const weight = $('#logWeight').value;
    const reps = $('#logReps').value;
    const rpe = $('#logRPE').value;

    // Mark as complete
    state.completedExercises.add(`${day}-${index}`);

    // In production, this would save to Google Sheets
    console.log('Saved:', { day, index, weight, reps, rpe });

    // Close modal and refresh
    modal.classList.remove('active');
    renderWorkoutList();
    showToast('Exercise logged! 💪');
}

// ===================================
// NUTRITION TAB
// ===================================

function renderNutritionTab() {
    const container = $('#nutritionSummary');
    const { nutritionLog } = state;

    container.innerHTML = `
    <div class="macro-card">
      <div class="macro-value">${nutritionLog.calories}</div>
      <div class="macro-label">Calories</div>
      <div class="macro-target">Target: ${NUTRITION_TARGETS.calories}</div>
    </div>
    <div class="macro-card">
      <div class="macro-value">${nutritionLog.protein}g</div>
      <div class="macro-label">Protein</div>
      <div class="macro-target">Target: ${NUTRITION_TARGETS.protein}g</div>
    </div>
    <div class="macro-card">
      <div class="macro-value">${nutritionLog.carbs}g</div>
      <div class="macro-label">Carbs</div>
      <div class="macro-target">Target: ${NUTRITION_TARGETS.carbs}g</div>
    </div>
    <div class="macro-card">
      <div class="macro-value">${nutritionLog.fat}g</div>
      <div class="macro-label">Fat</div>
      <div class="macro-target">Target: ${NUTRITION_TARGETS.fat}g</div>
    </div>
  `;
}

function initNutritionForm() {
    const form = $('#nutritionForm');
    form.addEventListener('submit', (e) => {
        e.preventDefault();

        state.nutritionLog = {
            calories: parseInt($('#calories').value) || 0,
            protein: parseInt($('#protein').value) || 0,
            carbs: parseInt($('#carbs').value) || 0,
            fat: parseInt($('#fat').value) || 0
        };

        renderNutritionTab();
        showToast('Nutrition saved! 🥗');
        form.reset();
    });
}

// ===================================
// RECOVERY TAB
// ===================================

function renderRecoveryTab() {
    // Yoga Flows
    $('#yogaFlows').innerHTML = RECOVERY_DATA.yoga_flows.map(item => `
    <div class="recovery-card" onclick="window.open('${item.url}', '_blank')">
      <div class="recovery-info">
        <h4>${item.name}</h4>
        <p>${item.description}</p>
      </div>
      <span class="recovery-duration">${item.duration}</span>
    </div>
  `).join('');

    // Stretching - expandable with individual exercises
    $('#stretchingRoutines').innerHTML = RECOVERY_DATA.stretching.map((routine, idx) => `
    <div class="stretching-routine">
      <div class="recovery-card" onclick="toggleStretchingRoutine(${idx})">
        <div class="recovery-info">
          <h4>${routine.name} <span style="font-size: 0.8em;">▼</span></h4>
          <p>${routine.description}</p>
        </div>
        <span class="recovery-duration">${routine.duration}</span>
      </div>
      <div class="stretch-exercises" id="stretch-routine-${idx}" style="display: none;">
        ${routine.exercises.map(ex => `
          <div class="stretch-item" onclick="event.stopPropagation(); window.open('${ex.url}', '_blank')">
            <div class="stretch-details">
              <span class="stretch-name">${ex.name}</span>
              <span class="stretch-cues">${ex.cues}</span>
            </div>
            <span class="stretch-duration">${ex.duration}</span>
          </div>
        `).join('')}
      </div>
    </div>
  `).join('');

    // Rest Day
    $('#restDayActivities').innerHTML = RECOVERY_DATA.rest_day.map(item => `
    <div class="recovery-card" ${item.url ? `onclick="window.open('${item.url}', '_blank')"` : ''}>
      <div class="recovery-info">
        <h4>${item.name}</h4>
        <p>${item.description}</p>
      </div>
    </div>
  `).join('');
}

// Toggle stretching routine expansion - must be global for onclick handlers
window.toggleStretchingRoutine = function (idx) {
    const el = document.getElementById(`stretch-routine-${idx}`);
    if (el) {
        if (el.style.display === 'none') {
            el.style.display = 'block';
        } else {
            el.style.display = 'none';
        }
    }
};

// ===================================
// PROGRESS TAB
// ===================================

function renderProgressTab() {
    $('#currentWeek').textContent = state.workoutData.current_week;

    // Populate Garmin Recovery Metrics
    const garmin = GARMIN_RECOVERY_DATA;
    $('#sleepScore').textContent = garmin.sleep_score ? `${garmin.sleep_score}/100` : '--';
    $('#sleepHours').textContent = garmin.sleep_duration_hours ? `${garmin.sleep_duration_hours}h` : '--';
    $('#bodyBattery').textContent = garmin.body_battery_current ? `${garmin.body_battery_current}%` : '--';
    $('#hrvStatus').textContent = garmin.hrv_status || '--';

    // Set recovery status message
    const recoveryStatus = $('#recoveryStatus');
    if (garmin.recovery_ready) {
        recoveryStatus.className = 'recovery-status ready';
        recoveryStatus.textContent = '✅ Recovery looks good - ready for intense training!';
    } else {
        recoveryStatus.className = 'recovery-status caution';
        recoveryStatus.textContent = '⚠️ Recovery metrics suggest taking it easier today';
    }

    const completedToday = [...state.completedExercises].filter(key => key.startsWith(state.selectedDay)).length;
    const totalToday = (state.workoutData[state.selectedDay] || []).length;

    $('#statsGrid').innerHTML = `
    <div class="stat-card">
      <div class="stat-value">${completedToday}/${totalToday}</div>
      <div class="stat-label">Today's Exercises</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">${state.completedExercises.size}</div>
      <div class="stat-label">Exercises This Week</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">145 lbs</div>
      <div class="stat-label">Hip Thrust PR</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">Week 2</div>
      <div class="stat-label">Current Week</div>
    </div>
  `;

    // Chart placeholder - would use Chart.js in production
    const canvas = $('#progressChart');
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#2a2a4a';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#888';
    ctx.font = '14px Inter';
    ctx.textAlign = 'center';
    ctx.fillText('Progress chart coming soon!', canvas.width / 2, canvas.height / 2);
}

// ===================================
// TOAST NOTIFICATION
// ===================================

function showToast(message) {
    const toast = $('#toast');
    toast.textContent = message;
    toast.classList.add('show');

    setTimeout(() => {
        toast.classList.remove('show');
    }, 2500);
}

// ===================================
// CHAT FUNCTIONALITY
// ===================================

function initChat() {
    const chatFab = $('#chatFab');
    const chatModal = $('#chatModal');
    const chatClose = $('#chatClose');
    const chatForm = $('#chatForm');

    // Toggle chat modal
    chatFab.addEventListener('click', () => {
        chatModal.classList.toggle('active');
    });

    chatClose.addEventListener('click', () => {
        chatModal.classList.remove('active');
    });

    // Handle chat form submission
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const input = $('#chatInput');
        const message = input.value.trim();

        if (!message) return;

        // Add user message to chat
        addChatMessage(message, 'user');
        input.value = '';

        // Show typing indicator
        showTypingIndicator();

        // Send to Gemini API
        try {
            const response = await sendToGemini(message);
            hideTypingIndicator();
            addChatMessage(response, 'assistant');
        } catch (error) {
            hideTypingIndicator();
            addChatMessage("Sorry, I couldn't process that. Please try again!", 'assistant');
            console.error('Chat error:', error);
        }
    });
}

function addChatMessage(text, type) {
    const messagesContainer = $('#chatMessages');
    const messageEl = document.createElement('div');
    messageEl.className = `chat-message ${type}`;
    messageEl.innerHTML = `<p>${text}</p>`;
    messagesContainer.appendChild(messageEl);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function showTypingIndicator() {
    const messagesContainer = $('#chatMessages');
    const typingEl = document.createElement('div');
    typingEl.className = 'chat-message assistant';
    typingEl.id = 'typingIndicator';
    typingEl.innerHTML = `
        <div class="chat-typing">
            <span></span><span></span><span></span>
        </div>
    `;
    messagesContainer.appendChild(typingEl);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function hideTypingIndicator() {
    const typingEl = $('#typingIndicator');
    if (typingEl) typingEl.remove();
}

async function sendToGemini(message) {
    // Get current context
    const cyclePhase = calculateCyclePhase();
    const today = new Date().toLocaleDateString('en-US', { weekday: 'long' });
    const todayWorkout = state.workoutData[today] || [];

    const context = `
You are Lianna's personal AI fitness coach. Be friendly, concise, and helpful.
Current context:
- Today is ${today}
- Cycle phase: ${cyclePhase.phase} (Day ${cyclePhase.day})
- Energy level: ${cyclePhase.energy}
- Training tip: ${cyclePhase.training_tip}
- Today's workout: ${todayWorkout.map(ex => ex.exercise).join(', ') || 'Rest day'}
- Her stats: Female, 5'2", 110 lbs, intermediate/advanced
- Gym: Planet Fitness (no barbells, has Smith machine, dumbbells, cables)
- Goals: Lose fat, gain muscle. Focus on glutes, back, triceps, obliques, quads, calves

Respond in 2-3 sentences max. Be supportive and knowledgeable.
`;

    // Call the serverless API
    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            message: message,
            context: context
        })
    });

    if (!response.ok) {
        throw new Error('Chat API error');
    }

    const data = await response.json();
    return data.response;
}

// Initialize chat on page load
document.addEventListener('DOMContentLoaded', () => {
    initChat();
});

// ===================================
// EXPORT FOR DEBUGGING
// ===================================

window.appState = state;

