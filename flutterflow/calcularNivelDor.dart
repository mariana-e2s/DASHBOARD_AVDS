import 'dart:convert';
import 'dart:math' as math;

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:intl/intl.dart';
import 'package:timeago/timeago.dart' as timeago;
import '/flutter_flow/custom_functions.dart';
import '/flutter_flow/lat_lng.dart';
import '/flutter_flow/place.dart';
import '/flutter_flow/uploaded_file.dart';
import '/backend/backend.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import '/auth/firebase_auth/auth_util.dart';

String calcularNivelDor(double intensidade) {
  /// MODIFY CODE ONLY BELOW THIS LINE

  if (intensidade <= 3) {
    return 'fraca';
  } else if (intensidade <= 7) {
    return 'media';
  } else {
    return 'alta';
  }

  /// MODIFY CODE ONLY ABOVE THIS LINE
}
