package com.sbomai.core.repository;

import com.sbomai.core.domain.SbomDocument;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.UUID;

@Repository
public interface SbomDocumentRepository extends JpaRepository<SbomDocument, UUID> {
    // Custom query methods can be added here
}
