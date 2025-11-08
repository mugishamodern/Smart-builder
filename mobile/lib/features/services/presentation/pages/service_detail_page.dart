import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:buildsmart_mobile/core/models/models.dart';
import 'package:buildsmart_mobile/shared/theme/app_theme.dart';
import 'package:url_launcher/url_launcher.dart';

/// Service detail page
/// 
/// Displays detailed information about a service and provider
class ServiceDetailPage extends ConsumerWidget {
  final ServiceModel service;

  const ServiceDetailPage({
    super.key,
    required this.service,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Service Details'),
        actions: [
          IconButton(
            icon: const Icon(Icons.share),
            onPressed: () {
              // TODO: Implement share functionality
            },
            tooltip: 'Share',
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Service header
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Container(
                          width: 64,
                          height: 64,
                          decoration: BoxDecoration(
                            color: AppTheme.primaryYellow.withValues(alpha: 0.1),
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: Icon(
                            _getServiceIcon(service.serviceType),
                            color: AppTheme.primaryYellow,
                            size: 32,
                          ),
                        ),
                        const SizedBox(width: 16),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                service.title,
                                style: const TextStyle(
                                  fontSize: 22,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              const SizedBox(height: 4),
                              Text(
                                service.serviceType
                                    .replaceAll('_', ' ')
                                    .toUpperCase(),
                                style: TextStyle(
                                  fontSize: 14,
                                  color: Colors.grey[600],
                                  fontWeight: FontWeight.w600,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),
                    if (service.description != null)
                      Text(service.description!),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Pricing
            Card(
              color: AppTheme.accentOrange.withValues(alpha: 0.1),
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text(
                      'Hourly Rate',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    Text(
                      'UGX ${service.hourlyRate.toStringAsFixed(2)}/hr',
                      style: TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                        color: AppTheme.accentOrange,
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Provider info
            if (service.provider != null) ...[
              const Text(
                'Service Provider',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 12),
              Card(
                child: ListTile(
                  leading: CircleAvatar(
                    backgroundColor: AppTheme.primaryYellow,
                    child: Text(
                      (service.provider!.fullName?.isNotEmpty == true
                              ? service.provider!.fullName![0]
                              : service.provider!.username[0])
                          .toUpperCase(),
                      style: const TextStyle(color: Colors.white),
                    ),
                  ),
                  title: Text(
                    service.provider!.fullName ?? service.provider!.username,
                    style: const TextStyle(fontWeight: FontWeight.bold),
                  ),
                  subtitle: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      if (service.provider!.email.isNotEmpty)
                        Text(service.provider!.email),
                      if (service.provider!.phone != null &&
                          service.provider!.phone!.isNotEmpty)
                        Text(service.provider!.phone!),
                    ],
                  ),
                  trailing: service.provider!.isVerified
                      ? const Icon(Icons.verified, color: Colors.blue)
                      : null,
                ),
              ),
              const SizedBox(height: 16),
            ],

            // Service details
            const Text(
              'Service Details',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 12),
            Card(
              child: Column(
                children: [
                  if (service.rating > 0)
                    ListTile(
                      leading: const Icon(Icons.star, color: Colors.amber),
                      title: const Text('Rating'),
                      trailing: Text(
                        '${service.rating.toStringAsFixed(1)} / 5.0',
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                    ),
                  if (service.yearsExperience > 0)
                    ListTile(
                      leading: const Icon(Icons.badge),
                      title: const Text('Experience'),
                      trailing: Text(
                        '${service.yearsExperience} years',
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                    ),
                  if (service.serviceArea != null)
                    ListTile(
                      leading: const Icon(Icons.location_on),
                      title: const Text('Service Area'),
                      trailing: Text(
                        service.serviceArea!,
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                    ),
                  if (service.certifications != null)
                    ListTile(
                      leading: const Icon(Icons.workspace_premium),
                      title: const Text('Certifications'),
                      subtitle: Text(service.certifications!),
                    ),
                ],
              ),
            ),
            const SizedBox(height: 16),

            // Portfolio link
            if (service.portfolioUrl != null)
              Card(
                child: ListTile(
                  leading: const Icon(Icons.link),
                  title: const Text('Portfolio'),
                  subtitle: Text(service.portfolioUrl!),
                  trailing: const Icon(Icons.open_in_new),
                  onTap: () async {
                    final url = Uri.parse(service.portfolioUrl!);
                    if (await canLaunchUrl(url)) {
                      await launchUrl(url, mode: LaunchMode.externalApplication);
                    }
                  },
                ),
              ),
            const SizedBox(height: 24),

            // Contact button
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: () {
                  // TODO: Implement contact functionality
                  // Show contact options (call, message, email)
                  showModalBottomSheet(
                    context: context,
                    builder: (context) => _ContactBottomSheet(
                      service: service,
                    ),
                  );
                },
                icon: const Icon(Icons.contact_support),
                label: const Text('Contact Provider'),
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  backgroundColor: AppTheme.accentOrange,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  IconData _getServiceIcon(String serviceType) {
    switch (serviceType.toLowerCase()) {
      case 'plumbing':
        return Icons.plumbing;
      case 'electrical':
        return Icons.electrical_services;
      case 'carpentry':
        return Icons.carpenter;
      case 'masonry':
        return Icons.construction;
      default:
        return Icons.build;
    }
  }
}

class _ContactBottomSheet extends StatelessWidget {
  final ServiceModel service;

  const _ContactBottomSheet({required this.service});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(24),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Text(
            'Contact Provider',
            style: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 24),
            if (service.provider?.phone != null)
            ListTile(
              leading: const Icon(Icons.phone),
              title: const Text('Call'),
              subtitle: Text(service.provider!.phone!),
              onTap: () async {
                final phone = service.provider!.phone;
                if (phone != null && phone.isNotEmpty) {
                  final url = Uri.parse('tel:$phone');
                  if (await canLaunchUrl(url)) {
                    await launchUrl(url);
                  }
                }
              },
            ),
          if (service.provider?.email != null)
            ListTile(
              leading: const Icon(Icons.email),
              title: const Text('Email'),
              subtitle: Text(service.provider!.email),
              onTap: () async {
                final email = service.provider!.email;
                if (email.isNotEmpty) {
                  final url = Uri.parse('mailto:$email');
                  if (await canLaunchUrl(url)) {
                    await launchUrl(url);
                  }
                }
              },
            ),
          const SizedBox(height: 16),
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
        ],
      ),
    );
  }
}

