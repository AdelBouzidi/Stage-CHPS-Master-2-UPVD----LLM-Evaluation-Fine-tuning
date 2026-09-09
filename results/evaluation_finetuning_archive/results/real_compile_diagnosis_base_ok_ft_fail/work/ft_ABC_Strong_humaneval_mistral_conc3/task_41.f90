program car_race_collision
  implicit none
  integer :: n
  integer :: collisions

  ! Read input
  read(*,*) n

  ! Calculate collisions
  collisions = n * n

  ! Output result
  print(*,*) collisions

end program car_race_collision