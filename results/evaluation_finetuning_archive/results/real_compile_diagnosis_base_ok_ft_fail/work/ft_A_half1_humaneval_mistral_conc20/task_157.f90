program right_angle_triangle_demo
  implicit none
  integer :: a, b, c
  logical :: result

  ! Read input
  read *, a
  read *, b
  read *, c

  ! Determine if it's a right-angled triangle
  result = right_angle_triangle(a, b, c)

  ! Output result
  print *, result

contains

  logical function right_angle_triangle(a, b, c)
    implicit none
    integer, intent(in) :: a, b, c
    integer :: sides(3)
    integer :: i, max_idx

    ! Store sides in array
    sides(1) = a
    sides(2) = b
    sides(3) = c

    ! Find the maximum side
    max_idx = 1
    do i = 2, 3
      if (sides(i) > sides(max_idx)) then
        max_idx = i
      end if
    end do

    ! Check Pythagorean theorem
    if (sides(max_idx)**2 == sides((max_idx+2)/3)**2 + sides((max_idx+1)/3)**2) then
      right_angle_triangle = .true.
    else
      right_angle_triangle = .false.
    end if
  end function right_angle_triangle

end program right_angle_triangle_demo