program main
  implicit none
  integer :: a
  integer :: root
  logical :: result

  read *, a

  root = int(a**(1.0/3.0))
  if (root**3 == a) then
    result = .true.
  else
    result = .false.
  end if

  print *, result
end program main